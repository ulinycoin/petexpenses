#!/usr/bin/env python3
"""AI slop detector and readability check for petexpenses.com HTML pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from common import extract_article_body_text, project_root, qa_data_dir


def load_blocklist(blocklist_path: Path) -> list[str]:
    if not blocklist_path.is_file():
        return [
            "in today's world",
            "it's important to note",
            "delve into",
            "landscape",
            "leverage",
            "comprehensive guide",
            "plays a crucial role",
            "at the end of the day",
            "when it comes to",
            "without further ado",
            "studies show",
            "research shows",
        ]

    phrases: list[str] = []
    for line in blocklist_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- ") and not line.startswith("- ["):
            phrase = line[2:].strip()
            phrase = re.split(r"\s+[\(\/]", phrase)[0].strip()
            if phrase:
                phrases.append(phrase.lower())
    return phrases


def count_syllables(word: str) -> int:
    word = word.lower().strip("'")
    if len(word) <= 3:
        return 1
    word = re.sub(r"e$", "", word)
    groups = re.findall(r"[aeiouy]+", word)
    return max(1, len(groups))


def calculate_flesch_en(text: str) -> dict[str, Any]:
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"\b[a-zA-Z'-]+\b", text)
    if not sentences or not words:
        return {"score": 100.0, "level": "Easy", "avg_sentence_len": 0.0}

    syllables = sum(count_syllables(w) for w in words)
    asl = len(words) / len(sentences)
    asw = syllables / len(words)
    score = 206.835 - 1.015 * asl - 84.6 * asw
    score = max(0.0, min(100.0, score))

    if score >= 70:
        level = "Easy (general web / consumer finance)"
    elif score >= 50:
        level = "Standard (editorial / explainer)"
    elif score >= 30:
        level = "Hard (technical / dense)"
    else:
        level = "Very hard (academic / legalese)"

    return {
        "score": round(score, 1),
        "level": level,
        "avg_sentence_len": round(asl, 1),
        "avg_syllables_per_word": round(asw, 2),
    }


def analyze_slop(html_path: Path, blocklist_path: Path) -> dict[str, Any]:
    html = html_path.read_text(encoding="utf-8")
    text = extract_article_body_text(html)
    text_lower = text.lower()
    blocklist = load_blocklist(blocklist_path)

    hits: list[dict[str, str]] = []
    for phrase in blocklist:
        pattern = re.compile(rf"\b{re.escape(phrase)}\b", re.IGNORECASE)
        for match in pattern.finditer(text_lower):
            start, end = match.span()
            hits.append(
                {
                    "phrase": phrase,
                    "context": text[max(0, start - 45) : min(len(text), end + 45)].strip(),
                }
            )

    over_long: list[dict[str, Any]] = []
    for sentence in re.split(r"[.!?]+", text):
        sentence = sentence.strip()
        if not sentence:
            continue
        word_count = len(re.findall(r"\b[a-zA-Z'-]+\b", sentence))
        if word_count > 28:
            over_long.append({"sentence": sentence, "word_count": word_count})

    readability = calculate_flesch_en(text)
    verdict = "pass"
    if len(hits) >= 1 or len(over_long) > 4 or readability["score"] < 35:
        verdict = "warning"
    if len(hits) >= 2:
        verdict = "fail"

    return {
        "source": html_path.relative_to(project_root()).as_posix(),
        "verdict": verdict,
        "total_slop_hits": len(hits),
        "slop_hits": hits,
        "total_over_long_sentences": len(over_long),
        "over_long_sentences": over_long[:10],
        "readability": readability,
        "word_count": len(re.findall(r"\b[a-zA-Z'-]+\b", text)),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="petexpenses.com AI slop detector")
    ap.add_argument("html", type=Path, nargs="+", help="HTML file(s) to scan")
    ap.add_argument("--blocklist", type=Path, default=None)
    ap.add_argument("-o", "--output", type=Path, help="Write JSON report")
    args = ap.parse_args()

    root = project_root()
    blocklist_path = args.blocklist or qa_data_dir() / "ai-slop-blocklist.md"
    if not blocklist_path.is_absolute():
        blocklist_path = root / blocklist_path

    reports: list[dict[str, Any]] = []
    worst = "pass"
    rank = {"pass": 0, "warning": 1, "fail": 2}

    for html in args.html:
        path = html if html.is_absolute() else root / html
        if not path.is_file():
            print(f"Not found: {path}", file=sys.stderr)
            return 2
        report = analyze_slop(path, blocklist_path)
        reports.append(report)
        if rank[report["verdict"]] > rank[worst]:
            worst = report["verdict"]

    payload = {"verdict": worst, "pages": reports}
    text = json.dumps(payload, ensure_ascii=False, indent=2)

    if args.output:
        out = args.output if args.output.is_absolute() else root / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")

    for report in reports:
        print(f"[{report['verdict'].upper()}] {report['source']}")
        print(f"  cliches: {report['total_slop_hits']}, long sentences: {report['total_over_long_sentences']}")
        print(f"  Flesch: {report['readability']['score']} — {report['readability']['level']}")
        for hit in report["slop_hits"][:5]:
            print(f"  - '{hit['phrase']}' …{hit['context']}…")

    return 0 if worst != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
