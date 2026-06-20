#!/usr/bin/env python3
"""Pre-deploy content QA gate for petexpenses.com.

Runs slop detection, cannibalization guard, and link verification across
blog posts and breed pages (or selected files).

Usage:
  python3 scripts/qa/check_content.py
  python3 scripts/qa/check_content.py --blog-only
  python3 scripts/qa/check_content.py blog/pet-insurance-worth-it.html
  python3 scripts/qa/check_content.py --remote   # also HTTP-check affiliate/external links
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import discover_content_pages, project_root


def run_module(module: str, args: list[str]) -> tuple[int, str]:
    script = Path(__file__).resolve().parent / module
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="petexpenses.com pre-deploy QA gate")
    ap.add_argument("html", type=Path, nargs="*", help="Optional specific HTML files")
    ap.add_argument("--blog-only", action="store_true")
    ap.add_argument("--breeds-only", action="store_true")
    ap.add_argument("--remote", action="store_true", help="HTTP-check affiliate/external links")
    ap.add_argument("--skip-cannibalization", action="store_true")
    ap.add_argument("-o", "--output", type=Path, help="Combined JSON summary path")
    args = ap.parse_args()

    root = project_root()
    reports_dir = root / "scripts/qa/reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    if args.html:
        pages = [p if p.is_absolute() else root / p for p in args.html]
    else:
        pages = discover_content_pages(
            include_blog=not args.breeds_only,
            include_breeds=not args.blog_only,
        )

    if not pages:
        print("No pages to check.", file=sys.stderr)
        return 2

    rel_paths = [p.relative_to(root).as_posix() for p in pages]
    summary: dict[str, object] = {"pages": rel_paths, "checks": {}}
    exit_code = 0

    slop_out = reports_dir / "slop-report.json"
    code, out = run_module("slop_detector.py", [*rel_paths, "-o", slop_out.as_posix()])
    summary["checks"]["slop"] = {"exit_code": code, "report": slop_out.relative_to(root).as_posix()}
    print(out)
    if code != 0:
        exit_code = max(exit_code, code)

    if not args.skip_cannibalization and not args.html:
        cannibal_args = ["-o", (reports_dir / "cannibalization-report.json").as_posix()]
        if args.blog_only:
            cannibal_args.insert(0, "--blog-only")
        if args.breeds_only:
            cannibal_args.insert(0, "--breeds-only")
        code, out = run_module("cannibalization_guard.py", cannibal_args)
        summary["checks"]["cannibalization"] = {
            "exit_code": code,
            "report": "scripts/qa/reports/cannibalization-report.json",
        }
        print("\n" + out)
        if code != 0:
            exit_code = max(exit_code, code)

    link_args = [*rel_paths, "-o", (reports_dir / "link-verify-report.json").as_posix()]
    if args.remote:
        link_args.append("--remote")
    else:
        link_args.append("--skip-external")
    code, out = run_module("link_verify.py", link_args)
    summary["checks"]["links"] = {
        "exit_code": code,
        "report": "scripts/qa/reports/link-verify-report.json",
    }
    print("\n" + out)
    if code != 0:
        exit_code = max(exit_code, code)

    summary["verdict"] = "pass" if exit_code == 0 else "fail"
    summary_text = json.dumps(summary, ensure_ascii=False, indent=2)

    out_path = args.output or reports_dir / "check-content-summary.json"
    if not out_path.is_absolute():
        out_path = root / out_path
    out_path.write_text(summary_text + "\n", encoding="utf-8")

    print(f"\nOverall: {summary['verdict'].upper()} (summary → {out_path.relative_to(root).as_posix()})")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
