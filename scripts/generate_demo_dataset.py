from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


FIELDNAMES = [
    "post_id",
    "text",
    "timestamp",
    "topic",
    "engagement_bait_label",
    "manipulation_labels",
    "claim_text",
    "claim_verdict",
    "source_url",
]

TOPICS = [
    "trade_policy",
    "conflict",
    "elections",
    "public_health",
    "economy",
    "diplomacy",
    "law_and_governance",
    "infrastructure",
    "public_finance",
    "environment",
    "education",
    "migration",
]

CLAIM_TEMPLATES = [
    "Officials reported that the {topic} program reached {number} percent completion.",
    "The ministry published a {topic} update covering {number} regional districts.",
    "The latest {topic} report recorded {number} new cases during the review period.",
    "The agency announced a {number} percent change in its {topic} budget.",
    "Independent observers documented {number} incidents related to {topic}.",
]

BAIT_PREFIXES = [
    "Share this now!",
    "Please repost before it disappears!",
    "Tag a friend and comment below!",
    "Like and share immediately!",
]

MANIPULATION_PREFIXES = [
    "Only real patriots will support this.",
    "The hidden elite are suppressing the report.",
    "This shocking decision will destroy everything.",
    "Choose one side or face the consequences.",
]


def build_rows(existing_rows: list[dict[str, str]], target_size: int) -> list[dict[str, str]]:
    rows = list(existing_rows)
    start_index = len(rows) + 1
    verdicts = [
        "supported_by_available_evidence",
        "contradicted_by_available_evidence",
        "mixed_or_context_dependent",
        "insufficient_evidence",
        "unverified",
    ]

    for offset in range(target_size - len(rows)):
        record_number = start_index + offset
        topic = TOPICS[offset % len(TOPICS)]
        number = 20 + (offset % 81)
        claim = CLAIM_TEMPLATES[offset % len(CLAIM_TEMPLATES)].format(topic=topic.replace("_", " "), number=number)
        is_bait = offset % 2 == 0
        is_manipulative = offset % 4 == 0

        if is_bait:
            text = f"{BAIT_PREFIXES[offset % len(BAIT_PREFIXES)]} {claim}"
            engagement_label = "1"
        elif is_manipulative:
            text = f"{MANIPULATION_PREFIXES[offset % len(MANIPULATION_PREFIXES)]} {claim}"
            engagement_label = "0"
        else:
            text = claim
            engagement_label = "0"

        labels = ""
        if is_bait:
            labels = "social_pressure"
        if is_manipulative:
            labels = "social_pressure;fear_appeal" if is_bait else "fear_appeal"

        timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc) + timedelta(days=offset)
        rows.append(
            {
                "post_id": f"p{record_number:03d}",
                "text": text,
                "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "topic": topic,
                "engagement_bait_label": engagement_label,
                "manipulation_labels": labels,
                "claim_text": claim,
                "claim_verdict": verdicts[offset % len(verdicts)],
                "source_url": f"https://example.com/demo-factcheck-{record_number}",
            }
        )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Expand the synthetic ASTMA demo dataset deterministically.")
    parser.add_argument("--input", type=Path, default=PROJECT_ROOT / "data/sample/sample_posts.csv")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--rows", type=int, default=500)
    args = parser.parse_args()

    if args.rows < 1:
        raise SystemExit("--rows must be positive")

    output_path = args.output or args.input
    with args.input.open("r", encoding="utf-8", newline="") as handle:
        existing_rows = list(csv.DictReader(handle))

    if len(existing_rows) > args.rows:
        raise SystemExit(f"Input already contains {len(existing_rows)} rows, more than requested {args.rows}.")

    rows = build_rows(existing_rows, args.rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()