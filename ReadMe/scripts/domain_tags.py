# -*- coding: utf-8 -*-
"""Map a free-text category / occupation string to one of our study domains.

Used by both the celebrity domain-signature analysis and the Wikidata pull, so
the two share one definition of "field". Keyword-based and order-sensitive
(first match wins) — tune the keyword lists as the corpus grows.
"""
from __future__ import annotations

# (domain, keywords) in priority order — first match wins.
_RULES = [
    ("Cinema",     ["actor", "actress", "filmmaker", "film director", "comedian",
                    "model", "animator", "director", "media mogul", "screenwriter"]),
    ("Music",      ["musician", "singer", "composer", "dancer", "rapper", "guitarist",
                    "pianist", "songwriter", "conductor"]),
    ("Sports",     ["cricket", "tennis", "badminton", "boxer", "boxing", "golf", "foot",
                    "sprint", "basketball", "athlete", "formula", "f1", "billiard",
                    "chess", "sportsperson", "racing", "shooter", "driver", "swimmer",
                    "wrestler", "cyclist"]),
    ("Science",    ["scientist", "physicist", "economist", "mathematician", "naturalist",
                    "astronomer", "inventor", "psychoanalyst", "psychiatrist", "chemist",
                    "biologist", "engineer", "researcher"]),
    ("Spiritual",  ["spiritual", "yogi", "yoga", "sage", "religious", "guru", "humanitarian",
                    "philosopher", "monk", "mystic", "saint", "theologian"]),
    ("Literature", ["author", "poet", "novelist", "writer", "playwright", "journalist"]),
    ("Business",   ["industrial", "entrepreneur", "tech executive", "business", "investor",
                    "ceo", "founder", "banker", "magnate"]),
    ("Politics",   ["president", "prime minister", "pm of", "politician", "monarch",
                    "chancellor", "secretary", "prince", "princess", "duke", "king",
                    "queen", "dictator", "emperor", "independence", "revolution",
                    "freedom", "leader", "diplomat", "activist", "statesman"]),
]


def domain_of(text: str) -> str:
    """Return the study-domain for a category/occupation string, or 'Other'."""
    c = (text or "").lower()
    for dom, keys in _RULES:
        if any(k in c for k in keys):
            return dom
    return "Other"


if __name__ == "__main__":
    for s in ("Actor & Filmmaker", "1st PM of India", "President & Scientist",
              "Yogi & Philosopher", "Poet & Freedom Fighter", "Businessman & Politician",
              "Tennis Player", "Media Mogul", "Naturalist"):
        print(f"  {s:28} -> {domain_of(s)}")
