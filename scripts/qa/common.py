"""Shared helpers for petexpenses.com content QA scripts."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

SITE_BASE = "https://petexpenses.com"

EN_STOP_WORDS = frozenset(
    """
    a an the and or but in on at to for of with by from as is are was were be been
    being have has had do does did will would could should may might must can this that
    these those it its they them their we you your our how much per year annual guide
    calculator free see real owning owner owners 2026 2025 updated
    """.split()
)

GENERIC_PET_WORDS = frozenset(
    """
    pet dog cat puppy kitten breed breeds owning own owner annual year yearly cost costs
    much does calculator guide free see real the a an per
    """.split()
)


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def qa_data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.h1 = ""
        self.h2s: list[str] = []
        self._in_title = False
        self._capture_tag: str | None = None
        self._capture_class: str | None = None
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
            self._buffer = []
        elif tag == "meta" and attr.get("name") == "description":
            self.description = attr.get("content", "").strip()
        elif tag == "link" and attr.get("rel") == "canonical":
            self.canonical = attr.get("href", "").strip()
        elif tag in ("h1", "h2"):
            classes = attr.get("class", "")
            if tag == "h1" and "article-h1" in classes.split():
                self._capture_tag = "h1"
                self._capture_class = "article-h1"
                self._buffer = []
            elif tag == "h2":
                self._capture_tag = "h2"
                self._capture_class = None
                self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self._in_title:
            self.title = "".join(self._buffer).strip()
            self._in_title = False
            self._buffer = []
        elif tag == "h1" and self._capture_tag == "h1":
            self.h1 = re.sub(r"\s+", " ", "".join(self._buffer)).strip()
            self._capture_tag = None
            self._buffer = []
        elif tag == "h2" and self._capture_tag == "h2":
            text = re.sub(r"\s+", " ", "".join(self._buffer)).strip()
            if text:
                self.h2s.append(text)
            self._capture_tag = None
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._in_title or self._capture_tag:
            self._buffer.append(data)


def strip_html(html: str) -> str:
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_article_body_text(html: str) -> str:
    match = re.search(
        r'<div class="article-body">(.*?)</div>\s*(?:<div class="article-cta"|</div>\s*<footer|</div>\s*</div>\s*<footer)',
        html,
        flags=re.I | re.S,
    )
    chunk = match.group(1) if match else html
    return strip_html(chunk)


def normalize_title(title: str) -> str:
    text = re.sub(r"\s*[—–-]\s*petexpenses\.com\s*$", "", title, flags=re.I)
    text = re.sub(r"\(\d{4}[^)]*\)", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_page_meta(html_path: Path) -> dict[str, Any]:
    html = html_path.read_text(encoding="utf-8")
    parser = _MetaParser()
    parser.feed(html)

    rel = html_path.relative_to(project_root()).as_posix()
    if rel.startswith("blog/") and html_path.name != "index.html":
        page_type = "blog"
        slug = html_path.stem
    elif rel.startswith("breeds/"):
        page_type = "breed"
        slug = html_path.stem
    else:
        page_type = "page"
        slug = html_path.stem

    primary = parser.h1 or normalize_title(parser.title)
    return {
        "path": rel,
        "slug": slug,
        "page_type": page_type,
        "title": parser.title,
        "primary_query": primary,
        "description": parser.description,
        "canonical": parser.canonical,
        "h1": parser.h1,
        "secondary_queries": parser.h2s[:8],
    }


def discover_content_pages(
    *,
    include_blog: bool = True,
    include_breeds: bool = True,
) -> list[Path]:
    root = project_root()
    paths: list[Path] = []
    if include_blog:
        blog_dir = root / "blog"
        if blog_dir.is_dir():
            paths.extend(
                sorted(p for p in blog_dir.glob("*.html") if p.name != "index.html")
            )
    if include_breeds:
        breeds_dir = root / "breeds"
        if breeds_dir.is_dir():
            paths.extend(sorted(breeds_dir.glob("*.html")))
    return paths


def normalize_tokens(text: str, *, drop_generic_pet: bool = False) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^\w\s'-]", " ", text)
    tokens: list[str] = []
    stop = EN_STOP_WORDS | (GENERIC_PET_WORDS if drop_generic_pet else frozenset())
    for word in text.split():
        w = word.strip("'")
        if len(w) < 3 or w in stop:
            continue
        stem = w[:5] if len(w) > 5 else w
        tokens.append(stem)
    return tokens


def token_set(text: str, *, drop_generic_pet: bool = False) -> set[str]:
    return set(normalize_tokens(text, drop_generic_pet=drop_generic_pet))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def url_to_local_path(href: str, root: Path | None = None) -> Path | None:
    root = root or project_root()
    href = href.split("#", 1)[0].strip()
    if not href:
        return None

    if href.startswith(("mailto:", "tel:", "javascript:")):
        return None

    if href.startswith("//"):
        href = "https:" + href

    if href.startswith("http://") or href.startswith("https://"):
        parsed_site = SITE_BASE.rstrip("/")
        if not href.startswith(parsed_site):
            return None
        href = href[len(parsed_site) :] or "/"

    if href.startswith("../"):
        # Resolve relative to blog/ — caller should pass html_path context; skip here.
        return None

    if not href.startswith("/"):
        return None

    path = href.rstrip("/")
    if path in ("", "/"):
        return root / "index.html"
    if path.endswith(".html"):
        return root / path.lstrip("/")

    # Directory-style URLs: /blog/ → blog/index.html
    index_candidate = root / path.lstrip("/") / "index.html"
    if index_candidate.is_file():
        return index_candidate

    return root / f"{path.lstrip('/')}.html"
