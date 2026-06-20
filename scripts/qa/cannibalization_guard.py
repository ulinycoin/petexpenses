#!/usr/bin/env python3
"""Keyword cannibalization guard for petexpenses.com blog + breed pages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from common import (
    discover_content_pages,
    extract_page_meta,
    jaccard,
    project_root,
    token_set,
)


def check_pair(
    a: dict[str, Any],
    b: dict[str, Any],
    *,
    threshold: float,
    cross_type_threshold: float,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    same_type = a["page_type"] == b["page_type"]
    limit = threshold if same_type else cross_type_threshold

    a_primary = token_set(a["primary_query"], drop_generic_pet=not same_type)
    b_primary = token_set(b["primary_query"], drop_generic_pet=not same_type)

    if a["primary_query"].strip().lower() == b["primary_query"].strip().lower():
        issues.append(
            {
                "severity": "fail",
                "type": "duplicate_primary_query",
                "message": (
                    f"Duplicate primary query between {a['path']} and {b['path']}: "
                    f"'{a['primary_query']}'"
                ),
                "pages": [a["path"], b["path"]],
                "similarity": 1.0,
            }
        )
        return issues

    sim = jaccard(a_primary, b_primary)
    if sim >= limit:
        issue_type = "high_primary_overlap" if same_type else "cross_type_cannibalization"
        severity = "fail" if same_type and sim >= 0.85 else "warning"
        issues.append(
            {
                "severity": severity,
                "type": issue_type,
                "message": (
                    f"{'Same-type' if same_type else 'Blog↔breed'} overlap "
                    f"({round(sim * 100)}%): '{a['primary_query']}' vs '{b['primary_query']}' "
                    f"({a['path']} ↔ {b['path']})"
                ),
                "pages": [a["path"], b["path"]],
                "queries": [a["primary_query"], b["primary_query"]],
                "similarity": round(sim, 2),
            }
        )

    for side, other, secondary_key in ((a, b, "secondary_queries"), (b, a, "secondary_queries")):
        other_primary = token_set(other["primary_query"], drop_generic_pet=True)
        for sec in side[secondary_key]:
            sec_tokens = token_set(sec, drop_generic_pet=True)
            sec_sim = jaccard(other_primary, sec_tokens)
            if sec_sim >= limit or other["primary_query"].strip().lower() == sec.strip().lower():
                issues.append(
                    {
                        "severity": "warning",
                        "type": "primary_secondary_overlap",
                        "message": (
                            f"Primary of {other['path']} overlaps secondary heading of {side['path']} "
                            f"({round(sec_sim * 100)}%): '{other['primary_query']}' vs '{sec}'"
                        ),
                        "pages": [side["path"], other["path"]],
                        "similarity": round(sec_sim, 2),
                    }
                )

    return issues


def check_cannibalization(
    pages: list[dict[str, Any]],
    *,
    threshold: float,
    cross_type_threshold: float,
) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    verdict = "pass"

    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            pair_issues = check_pair(
                pages[i],
                pages[j],
                threshold=threshold,
                cross_type_threshold=cross_type_threshold,
            )
            issues.extend(pair_issues)

    for issue in issues:
        if issue["severity"] == "fail":
            verdict = "fail"
        elif issue["severity"] == "warning" and verdict != "fail":
            verdict = "warning"

    return {
        "verdict": verdict,
        "pages_checked": len(pages),
        "threshold_same_type": threshold,
        "threshold_cross_type": cross_type_threshold,
        "total_issues": len(issues),
        "issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="petexpenses.com cannibalization guard")
    ap.add_argument("--threshold", type=float, default=0.72, help="Same-type Jaccard warn threshold")
    ap.add_argument(
        "--cross-threshold",
        type=float,
        default=0.55,
        help="Blog↔breed Jaccard warn threshold (after generic word drop)",
    )
    ap.add_argument("--blog-only", action="store_true")
    ap.add_argument("--breeds-only", action="store_true")
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args()

    root = project_root()
    html_paths = discover_content_pages(
        include_blog=not args.breeds_only,
        include_breeds=not args.blog_only,
    )
    if not html_paths:
        print("No content pages found.", file=sys.stderr)
        return 2

    pages = [extract_page_meta(p) for p in html_paths]
    report = check_cannibalization(
        pages,
        threshold=args.threshold,
        cross_type_threshold=args.cross_threshold,
    )

    text = json.dumps(report, ensure_ascii=False, indent=2)
    output = args.output or root / "scripts/qa/reports/cannibalization-report.json"
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text + "\n", encoding="utf-8")

    print(f"Cannibalization verdict: {report['verdict'].upper()}")
    print(f"Pages checked: {report['pages_checked']}, issues: {report['total_issues']}")
    print(f"Report: {output.relative_to(root).as_posix()}")

    for issue in report["issues"][:20]:
        prefix = "[FAIL]" if issue["severity"] == "fail" else "[WARN]"
        print(f" {prefix} {issue['message']}")
    if len(report["issues"]) > 20:
        print(f" … and {len(report['issues']) - 20} more (see JSON)")

    return 0 if report["verdict"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
