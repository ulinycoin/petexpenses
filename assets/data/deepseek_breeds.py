#!/usr/bin/env python3
"""Generate unique intro + savings for top GSC breed pages via DeepSeek.

Usage:
  python3 assets/data/deepseek_breeds.py
  python3 assets/data/deepseek_breeds.py --refresh
  python3 assets/data/deepseek_breeds.py --breed Bulldog

Writes cache: scripts/.cache/deepseek/{slug}.json
Updates:      assets/data/breeds_deepseek_content.py
Then run:     python3 assets/data/generate_breeds.py --all
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
CACHE_DIR = os.path.join(ROOT, "scripts", ".cache", "deepseek")
OUTPUT = os.path.join(SCRIPT_DIR, "breeds_deepseek_content.py")

sys.path.insert(0, SCRIPT_DIR)
from breeds_data import DOG_BREEDS, CAT_BREEDS  # noqa: E402

try:
    import certifi

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

API_URL = "https://api.deepseek.com/v1/chat/completions"

# Top 20 breed pages by GSC impressions (May 2026)
TOP_BREEDS: list[tuple[str, str]] = [
    ("Sphynx", "cat"),
    ("Siberian Husky", "dog"),
    ("Rottweiler", "dog"),
    ("Pomeranian", "dog"),
    ("Dachshund", "dog"),
    ("Boxer", "dog"),
    ("Poodle", "dog"),
    ("Siamese", "cat"),
    ("Maine Coon", "cat"),
    ("British Shorthair", "cat"),
    ("Labrador Retriever", "dog"),
    ("Bulldog", "dog"),
    ("Ragdoll", "cat"),
    ("Persian", "cat"),
    ("French Bulldog", "dog"),
    ("Devon Rex", "cat"),
    ("Russian Blue", "cat"),
    ("Chihuahua", "dog"),
    ("Domestic Shorthair", "cat"),
    ("American Shorthair", "cat"),
]

SYSTEM = (
    "You write factual US pet ownership cost guides for petexpenses.com. "
    "Tone: direct, helpful, 2026 data. No fluff, no emojis. "
    "Return ONLY valid JSON — no markdown fences, no commentary."
)


def load_dotenv() -> None:
    for base in [ROOT, os.path.join(ROOT, "..")]:
        path = os.path.join(base, ".env")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def make_slug(name: str) -> str:
    slug = name.lower()
    slug = slug.replace(" (pembroke)", "-pembroke")
    slug = slug.replace("'", "")
    slug = slug.replace(" & ", "-and-")
    slug = re.sub(r"[^a-z0-9-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug + "-cost"


def cost_range(name: str, species: str) -> tuple[int, int, str, str]:
    from generate_breeds import build_args  # noqa: WPS433

    data = DOG_BREEDS[name] if species == "dog" else CAT_BREEDS[name]
    args = build_args(name, data, species)
    lo = int(args["COST_LOW"].replace(",", ""))
    hi = int(args["COST_HIGH"].replace(",", ""))
    return lo, hi, data[6], args["SIZE_DESC"]


def deepseek_chat(prompt: str, temperature: float = 0.55) -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        sys.stderr.write("DEEPSEEK_API_KEY missing — add to .env\n")
        sys.exit(1)

    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=120, context=SSL_CONTEXT) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(5)
                continue
            err = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"API {e.code}: {err}") from e


def parse_json(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def validate_content(data: dict, lo: int, hi: int) -> dict:
    intro = data.get("intro", "").strip()
    savings = data.get("savings", [])
    if not intro or len(intro.split()) < 25:
        raise ValueError("intro too short")
    if len(intro.split()) > 220:
        raise ValueError("intro too long")
    if len(savings) != 5:
        raise ValueError(f"expected 5 savings tips, got {len(savings)}")
    tips = []
    for item in savings:
        title = str(item.get("title", "")).strip().rstrip(".")
        body = str(item.get("body", "")).strip()
        if not title or not body:
            raise ValueError("empty savings item")
        tips.append((title, body))
    # Block wildly wrong annual totals in intro (allow generic ranges like $300–$800)
    wrong = re.findall(r"\$[\d,]+(?:\s*[–-]\s*\$[\d,]+)?/year", intro)
    for m in wrong:
        nums = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", m)]
        if len(nums) >= 2 and (nums[0] < lo * 0.5 or nums[1] > hi * 1.5):
            raise ValueError(f"intro cites out-of-range annual cost: {m}")
    return {"intro": intro, "savings": tips}


def build_prompt(name: str, species: str, lo: int, hi: int, health: str, size_desc: str) -> str:
    species_word = "cat" if species == "cat" else "dog"
    return f"""Breed: {name} ({species_word})
Size: {size_desc}
Annual ownership cost (verified): ${lo:,}–${hi:,}/year — use ONLY this range if citing totals
Health note: {health}

Write JSON with exactly this shape:
{{
  "intro": "2-3 sentences, 40-80 words. US audience. Focus on ANNUAL ownership costs only — no puppy purchase price. Mention one breed-specific cost driver.",
  "savings": [
    {{"title": "short tip headline", "body": "1-2 sentences, breed-specific, actionable"}},
    ...5 items total, all different from generic pet advice
  ]
}}"""


def generate_one(name: str, species: str, refresh: bool = False) -> dict:
    slug = make_slug(name)
    cache_path = os.path.join(CACHE_DIR, f"{slug}.json")
    if os.path.isfile(cache_path) and not refresh:
        with open(cache_path, encoding="utf-8") as f:
            return json.load(f)

    lo, hi, health, size_desc = cost_range(name, species)
    prompt = build_prompt(name, species, lo, hi, health, size_desc)

    for attempt in range(3):
        raw = deepseek_chat(prompt, temperature=0.55 if attempt == 0 else 0.45)
        try:
            parsed = validate_content(parse_json(raw), lo, hi)
            break
        except (json.JSONDecodeError, ValueError) as e:
            if attempt == 2:
                raise
            prompt = (
                f"Previous output invalid ({e}). Return ONLY valid JSON.\n\n" + prompt
            )

    result = {"name": name, "species": species, "slug": slug, **parsed}
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


def write_output(results: list[dict]) -> None:
    hooks: dict[str, str] = {}
    savings: dict[str, list[tuple[str, str]]] = {}
    for r in results:
        hooks[r["name"]] = r["intro"]
        savings[r["name"]] = r["savings"]

    lines = [
        '"""Auto-generated by deepseek_breeds.py — do not edit by hand."""',
        "",
        "BREED_HOOKS_DEEPSEEK = " + repr(hooks),
        "",
        "BREED_SAVINGS = " + repr(savings),
        "",
    ]
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUTPUT} ({len(results)} breeds)")


def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser()
    p.add_argument("--refresh", action="store_true", help="Ignore cache")
    p.add_argument("--breed", help="Single breed name, e.g. Bulldog")
    args = p.parse_args()

    breeds = TOP_BREEDS
    if args.breed:
        found = None
        for name, sp in TOP_BREEDS:
            if name.lower() == args.breed.lower():
                found = (name, sp)
                break
        if not found:
            sp = "dog" if args.breed in DOG_BREEDS else "cat" if args.breed in CAT_BREEDS else None
            if not sp:
                sys.exit(f"Unknown breed: {args.breed}")
            found = (args.breed, sp)
        breeds = [found]

    results: list[dict] = []
    for i, (name, species) in enumerate(breeds):
        slug = make_slug(name)
        print(f"[{i + 1}/{len(breeds)}] {name} ({species})...", flush=True)
        try:
            results.append(generate_one(name, species, refresh=args.refresh))
        except Exception as e:
            print(f"  FAIL: {e}", file=sys.stderr)
            sys.exit(1)
        if i < len(breeds) - 1:
            time.sleep(1)

    # Merge with existing cache for breeds not in this run
    if os.path.isdir(CACHE_DIR):
        for fname in os.listdir(CACHE_DIR):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(CACHE_DIR, fname)
            with open(path, encoding="utf-8") as f:
                cached = json.load(f)
            if cached["name"] not in {r["name"] for r in results}:
                results.append(cached)

    results.sort(key=lambda r: r["name"])
    write_output(results)


if __name__ == "__main__":
    main()
