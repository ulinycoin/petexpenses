#!/usr/bin/env python3
"""Verify internal, affiliate, and external links in petexpenses.com HTML."""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

from common import SITE_BASE, project_root, url_to_local_path

USER_AGENT = "PetExpensesLinkVerify/1.0"
AFFILIATE_HOSTS = frozenset(
    {
        "awin1.com",
        "www.awin1.com",
        "shareasale.com",
        "www.shareasale.com",
        "impactradius-go.com",
        "prf.hn",
    }
)


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attr = {k: (v or "") for k, v in attrs}
        href = attr.get("href", "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            return
        self.links.append(href)


def extract_links(html: str) -> list[str]:
    parser = LinkExtractor()
    parser.feed(html)
    seen: set[str] = set()
    out: list[str] = []
    for href in parser.links:
        if href not in seen:
            seen.add(href)
            out.append(href)
    return out


def classify_link(href: str) -> str:
    if href.startswith("/") or (not urlparse(href).scheme and not href.startswith("http")):
        return "internal"
    host = urlparse(href).netloc.lower()
    if host in AFFILIATE_HOSTS:
        return "affiliate"
    if href.startswith(SITE_BASE):
        return "internal"
    return "external"


def resolve_local(href: str, html_path: Path, root: Path) -> Path | None:
    bare = href.split("#", 1)[0].strip()
    if bare.startswith(("http://", "https://")):
        parsed = urlparse(bare)
        if parsed.netloc and parsed.netloc not in ("petexpenses.com", "www.petexpenses.com"):
            return None
        bare = parsed.path or "/"
        if parsed.query:
            bare = f"{bare}?{parsed.query}"

    # Calculator deep links: /?breed=Labrador → index.html (query preserved in href, file exists)
    path_only = bare.split("?", 1)[0] or "/"
    if path_only in ("/", "/index.html"):
        index = root / "index.html"
        return index if index.is_file() else None

    if bare.startswith("/"):
        return url_to_local_path(path_only, root)

    # Relative to current file (blog/foo.html → ../breeds/bar-cost.html)
    if not href.startswith("../") and not href.startswith("./"):
        # treat as site-root relative without leading slash
        candidate = root / href.lstrip("/")
        if candidate.is_file():
            return candidate
        html_candidate = root / f"{href.lstrip('/')}.html"
        return html_candidate if html_candidate.is_file() else None

    return (html_path.parent / href).resolve()


def check_local_file(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"ok": False, "error": "could not resolve local path"}
    if path.is_file():
        return {"ok": True, "local_path": path.relative_to(project_root()).as_posix(), "error": None}
    return {"ok": False, "local_path": str(path), "error": "file not found"}


def check_url(url: str, timeout: float) -> dict[str, Any]:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return {"status": resp.status, "ok": 200 <= resp.status < 400, "method": "HEAD", "error": None}
    except urllib.error.HTTPError as e:
        if e.code in (405, 501, 403):
            return _get_fallback(url, timeout, ctx, str(e))
        return {"status": e.code, "ok": False, "method": "HEAD", "error": str(e)}
    except Exception as e:  # noqa: BLE001
        return _get_fallback(url, timeout, ctx, str(e))


def _get_fallback(url: str, timeout: float, ctx: ssl.SSLContext, head_error: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return {
                "status": resp.status,
                "ok": 200 <= resp.status < 400,
                "method": "GET",
                "error": None if resp.status < 400 else head_error,
            }
    except urllib.error.HTTPError as e:
        return {"status": e.code, "ok": False, "method": "GET", "error": str(e)}
    except Exception as e:  # noqa: BLE001
        return {"status": None, "ok": False, "method": "GET", "error": str(e)}


def verify_html(
    html_path: Path,
    *,
    check_remote: bool,
    skip_external: bool,
    timeout: float,
) -> dict[str, Any]:
    root = project_root()
    html = html_path.read_text(encoding="utf-8")
    links = extract_links(html)
    results: list[dict[str, Any]] = []

    for href in links:
        kind = classify_link(href)
        entry: dict[str, Any] = {"href": href, "kind": kind, "skipped": False}

        if kind == "internal":
            local = resolve_local(href, html_path, root)
            local_result = check_local_file(local)
            entry.update(local_result)
            entry["check"] = "local_file"
            results.append(entry)
            continue

        if kind == "affiliate":
            if check_remote:
                absolute = href if href.startswith("http") else urljoin(SITE_BASE + "/", href)
                remote = check_url(absolute, timeout)
                entry.update(remote)
                entry["check"] = "http"
            else:
                entry.update({"ok": True, "check": "affiliate_present", "error": None})
            results.append(entry)
            continue

        if skip_external:
            entry.update({"ok": True, "skipped": True, "check": "skipped_external"})
            results.append(entry)
            continue

        if check_remote:
            remote = check_url(href, timeout)
            entry.update(remote)
            entry["check"] = "http"
        else:
            entry.update({"ok": True, "skipped": True, "check": "external_not_checked"})
        results.append(entry)

    failed = [r for r in results if not r.get("ok")]
    return {
        "source": html_path.relative_to(root).as_posix(),
        "total_links": len(results),
        "failed_count": len(failed),
        "verdict": "pass" if not failed else "fail",
        "links": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="petexpenses.com link verifier")
    ap.add_argument("html", type=Path, nargs="+", help="HTML file(s)")
    ap.add_argument("-o", "--output", type=Path, help="Write JSON report")
    ap.add_argument("--remote", action="store_true", help="HTTP-check affiliate + external links")
    ap.add_argument("--skip-external", action="store_true", help="Skip external HTTP checks")
    ap.add_argument("--timeout", type=float, default=15.0)
    args = ap.parse_args()

    root = project_root()
    reports: list[dict[str, Any]] = []
    worst = "pass"

    for html in args.html:
        path = html if html.is_absolute() else root / html
        if not path.is_file():
            print(f"Not found: {path}", file=sys.stderr)
            return 2
        report = verify_html(
            path,
            check_remote=args.remote,
            skip_external=args.skip_external,
            timeout=args.timeout,
        )
        reports.append(report)
        if report["verdict"] == "fail":
            worst = "fail"

    payload = {"verdict": worst, "pages": reports}
    text = json.dumps(payload, ensure_ascii=False, indent=2)

    if args.output:
        out = args.output if args.output.is_absolute() else root / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")

    for report in reports:
        print(f"[{report['verdict'].upper()}] {report['source']} — {report['failed_count']} broken / {report['total_links']} links")
        for link in report["links"]:
            if not link.get("ok"):
                print(f"  ✗ {link['href']} ({link.get('error') or link.get('status')})")

    return 0 if worst == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
