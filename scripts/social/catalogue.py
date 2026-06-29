"""Content catalogue for social publishing."""

from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass
from typing import Literal

from .common import BASE_DIR, is_published

Species = Literal["Dog", "Cat"]
ItemType = Literal["blog", "breed"]


@dataclass(frozen=True)
class SocialItem:
    key: str
    item_type: ItemType
    title: str
    url: str
    badge: str
    message: str
    pin_title: str
    pin_description: str
    species: Species = "Dog"
    board_key: str = "budgeting"

    @property
    def pinterest_board_key(self) -> str:
        if self.item_type == "breed":
            return "dog-breeds" if self.species == "Dog" else "cat-calculator"
        return self.board_key


BLOG_ITEMS: list[SocialItem] = [
    SocialItem(
        key="pet-insurance",
        item_type="blog",
        title="Is Pet Insurance Worth It?",
        url="https://petexpenses.com/blog/pet-insurance-worth-it",
        badge="PET INSURANCE",
        message=(
            "Is pet insurance actually worth the monthly premium? I ran the numbers on 12 breeds. "
            "For French Bulldogs, Goldens, and other high-risk breeds it pays for itself.\n\n"
            "Read the full analysis → petexpenses.com/blog/pet-insurance-worth-it"
        ),
        pin_title="Is Pet Insurance Worth It? (2026 Cost Analysis)",
        pin_description=(
            "Do you really need pet insurance? Compare vet costs by breed and see how much "
            "pet insurance saves per year. Free calculator at petexpenses.com."
        ),
        board_key="pet-insurance",
    ),
    SocialItem(
        key="new-puppy",
        item_type="blog",
        title="New Puppy First Year Cost",
        url="https://petexpenses.com/blog/new-puppy-first-year-cost",
        badge="PUPPY BUDGET",
        message=(
            "Bringing home a puppy? The first year can cost $1,500–$5,000+ depending on breed. "
            "Here's exactly where the money goes — vaccinations, crate, training, food, and vet visits.\n\n"
            "Full breakdown → petexpenses.com/blog/new-puppy-first-year-cost"
        ),
        pin_title="New Puppy First Year Cost (2026 Guide)",
        pin_description=(
            "Budget for your puppy's first year: vaccines, crate, training, food, and vet visits. "
            "Real 2026 cost breakdown for new dog owners."
        ),
        species="Dog",
        board_key="dog-calculator",
    ),
    SocialItem(
        key="cheapest-breeds",
        item_type="blog",
        title="Cheapest Dog Breeds to Own",
        url="https://petexpenses.com/blog/cheapest-dog-breeds-to-own",
        badge="BUDGET BREEDS",
        message=(
            "Not all dogs cost the same. Some breeds cost under $1,000/year while others hit $3,500+. "
            "Here are the most budget-friendly breeds and why they're cheaper.\n\n"
            "See the list → petexpenses.com/blog/cheapest-dog-breeds-to-own"
        ),
        pin_title="Cheapest Dog Breeds to Own in 2026",
        pin_description=(
            "Which dog breeds cost the least per year? Compare annual food, vet, grooming, "
            "and insurance costs for budget-friendly breeds."
        ),
        species="Dog",
        board_key="dog-breeds",
    ),
    SocialItem(
        key="vet-visit-costs",
        item_type="blog",
        title="Dog Vet Visit Costs",
        url="https://petexpenses.com/blog/dog-vet-visit-costs",
        badge="VET COSTS",
        message=(
            "A routine vet visit runs $50–$250. An emergency? Can hit $5,000 overnight. "
            "Here's what 12 common procedures actually cost and how pet insurance changes the math.\n\n"
            "Full guide → petexpenses.com/blog/dog-vet-visit-costs"
        ),
        pin_title="Dog Vet Visit Costs — 2026 Price Guide",
        pin_description=(
            "How much does a dog vet visit cost? Routine checkups, vaccines, emergencies, "
            "and surgery prices with insurance math."
        ),
        species="Dog",
        board_key="pet-insurance",
    ),
    SocialItem(
        key="kibble-vs-fresh",
        item_type="blog",
        title="Kibble vs Fresh vs Raw: Cost Showdown",
        url="https://petexpenses.com/blog/kibble-vs-fresh-vs-raw",
        badge="FOOD COSTS",
        message=(
            "Kibble: $200/year. Fresh: $2,800/year. Raw: $3,500+/year. "
            "Is premium food worth it or is kibble fine? I compared costs, nutrition, and vet opinions.\n\n"
            "Read the comparison → petexpenses.com/blog/kibble-vs-fresh-vs-raw"
        ),
        pin_title="Kibble vs Fresh vs Raw Dog Food Costs",
        pin_description=(
            "Annual dog food cost comparison: kibble, fresh, and raw diets. "
            "Which option is worth the price in 2026?"
        ),
        species="Dog",
        board_key="budgeting",
    ),
    SocialItem(
        key="dog-food-recalls",
        item_type="blog",
        title="Dog Food Recalls 2026 — Brands to Avoid",
        url="https://petexpenses.com/blog/dog-food-recalls-2026",
        badge="SAFETY ALERT",
        message=(
            "50+ dog food recalls in 2026 so far. Some of the biggest brands made the list. "
            "Here's which ones had issues and safer alternatives with clean track records.\n\n"
            "Check the list → petexpenses.com/blog/dog-food-recalls-2026"
        ),
        pin_title="Dog Food Recalls 2026 — Brands to Avoid",
        pin_description=(
            "Updated list of 2026 dog food recalls. See which brands had safety issues "
            "and find safer alternatives for your dog."
        ),
        species="Dog",
        board_key="budgeting",
    ),
    SocialItem(
        key="litter-box-cost",
        item_type="blog",
        title="Self-Cleaning Litter Box Cost",
        url="https://petexpenses.com/blog/self-cleaning-litter-box-cost",
        badge="CAT GEAR",
        message=(
            "Automatic litter boxes cost $200–$800 upfront but save on litter over time. "
            "I tested a MeoWant and crunched the 3-year cost vs traditional boxes.\n\n"
            "See the math → petexpenses.com/blog/self-cleaning-litter-box-cost"
        ),
        pin_title="Self-Cleaning Litter Box Cost — Worth It?",
        pin_description=(
            "Compare automatic vs traditional litter box costs over 3 years. "
            "Upfront price, litter savings, and maintenance for cat owners."
        ),
        species="Cat",
        board_key="cat-calculator",
    ),
    SocialItem(
        key="understanding-costs",
        item_type="blog",
        title="Understanding Pet Costs — Complete Guide",
        url="https://petexpenses.com/blog/understanding-pet-costs",
        badge="COST GUIDE",
        message=(
            "Americans spend $1,000–$5,000/year on a single pet. Most people underestimate costs by 40%. "
            "Here's a complete breakdown of every expense category.\n\n"
            "Read the guide → petexpenses.com/blog/understanding-pet-costs"
        ),
        pin_title="Understanding Pet Costs — Complete 2026 Guide",
        pin_description=(
            "Full breakdown of annual pet expenses: food, vet, insurance, grooming, and supplies. "
            "Stop underestimating what your pet really costs."
        ),
        board_key="budgeting",
    ),
    SocialItem(
        key="cat-cost-per-year",
        item_type="blog",
        title="Cat Cost Per Year (2026)",
        url="https://petexpenses.com/blog/cat-cost-per-year-2026",
        badge="CAT BUDGET",
        message=(
            "How much does a cat cost per year in 2026? Food, litter, vet, insurance, and supplies "
            "add up faster than most owners expect. Here's the real annual breakdown.\n\n"
            "See the numbers → petexpenses.com/blog/cat-cost-per-year-2026"
        ),
        pin_title="How Much Does a Cat Cost Per Year? (2026)",
        pin_description=(
            "Annual cat ownership costs in 2026: food, litter, vet care, insurance, and supplies. "
            "Budget calculator for cat parents."
        ),
        species="Cat",
        board_key="cat-calculator",
    ),
]


def _slug_to_name(slug: str) -> str:
    return slug.replace("-", " ").title().replace("Corgi Pembroke", "Corgi (Pembroke)")


def _species_for_slug(slug: str) -> Species:
    cat_slugs = {
        "abyssinian", "american-shorthair", "bengal", "birman", "british-shorthair",
        "burmese", "cornish-rex", "devon-rex", "domestic-longhair", "domestic-shorthair",
        "exotic-shorthair", "maine-coon", "manx", "norwegian-forest-cat", "oriental-shorthair",
        "persian", "ragdoll", "russian-blue", "savannah", "scottish-fold", "siamese",
        "sphynx", "tonkinese",
    }
    return "Cat" if slug in cat_slugs else "Dog"


def _article(name: str) -> str:
    return "an" if name[:1].lower() in "aeiou" else "a"


def discover_breeds() -> list[SocialItem]:
    breeds_dir = os.path.join(BASE_DIR, "breeds")
    items: list[SocialItem] = []
    for path in sorted(glob.glob(os.path.join(breeds_dir, "*-cost.html"))):
        filename = os.path.basename(path)
        slug = filename.replace("-cost.html", "")
        name = _slug_to_name(slug)
        article = _article(name)
        species = _species_for_slug(slug)
        url = f"https://petexpenses.com/breeds/{slug}-cost"
        title = f"How Much Does {article} {name} Cost?"
        items.append(
            SocialItem(
                key=slug,
                item_type="breed",
                title=title,
                url=url,
                badge=f"{species.upper()} COST",
                message=(
                    f"How much does a {name} cost per year? Food, vet, insurance, grooming — "
                    f"see the real 2026 breakdown with a free breed calculator.\n\n"
                    f"Calculate now → petexpenses.com/breeds/{slug}-cost"
                ),
                pin_title=f"{name} Annual Cost (2026 Guide)",
                pin_description=(
                    f"See the real annual cost of owning a {name} in 2026. "
                    f"Food, vet, insurance, grooming & supplies. Free breed-specific calculator."
                ),
                species=species,
            )
        )
    return items


def all_items(item_type: ItemType | None = None) -> list[SocialItem]:
    items = list(BLOG_ITEMS) + discover_breeds()
    if item_type:
        items = [item for item in items if item.item_type == item_type]
    return items


def get_item(key: str) -> SocialItem | None:
    for item in all_items():
        if item.key == key:
            return item
    return None


def next_unpublished(
    channel: str,
    *,
    item_type: ItemType | None = None,
    prefer_blogs: bool = True,
) -> SocialItem | None:
    return next_for_channels([channel], item_type=item_type, prefer_blogs=prefer_blogs)


def needs_publish(channels: list[str], key: str) -> bool:
    return all(not is_published(channel, key) for channel in channels)


def next_for_channels(
    channels: list[str],
    *,
    item_type: ItemType | None = None,
    prefer_blogs: bool = True,
) -> SocialItem | None:
    """First catalogue item unpublished on any of the given channels."""

    def first_unpublished(items: list[SocialItem]) -> SocialItem | None:
        for item in items:
            if needs_publish(channels, item.key):
                return item
        return None

    blogs = all_items("blog")
    breeds = all_items("breed")

    if item_type == "blog":
        return first_unpublished(blogs)
    if item_type == "breed":
        return first_unpublished(breeds)

    if prefer_blogs:
        found = first_unpublished(blogs)
        if found:
            return found
    return first_unpublished(breeds) or first_unpublished(blogs)


def parse_meta_description(html_path: str) -> str | None:
    if not os.path.exists(html_path):
        return None
    with open(html_path, "r", encoding="utf-8") as handle:
        content = handle.read(4000)
    match = re.search(r'<meta name="description" content="([^"]+)"', content)
    return match.group(1) if match else None
