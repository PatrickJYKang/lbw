import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_PATH = Path(__file__).with_name("data.json")


def _parse_timestamp(timestamp: str) -> int:
    """Convert HH:MM:SS string to seconds."""
    parts = timestamp.split(":")
    if len(parts) != 3:
        raise ValueError(f"Timestamp must be HH:MM:SS, got: {timestamp}")
    hours, minutes, seconds = map(int, parts)
    return hours * 3600 + minutes * 60 + seconds


def _build_link(base_url: str, timestamp: str) -> str:
    seconds = _parse_timestamp(timestamp)
    separator = "&" if "?" in base_url else "?"
    return f"{base_url}{separator}t={seconds}s"


def _collect_deliveries(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    options: List[Dict[str, Any]] = []
    for video in data.get("videos", []):
        youtube_url = video.get("youtube_url")
        if not youtube_url:
            continue
        for delivery in video.get("deliveries", []):
            delivery_clip: Optional[Dict[str, Any]] = None
            review_clip: Optional[Dict[str, Any]] = None
            for clip in delivery.get("clips", []):
                if clip.get("type") == "delivery" and delivery_clip is None:
                    delivery_clip = clip
                elif clip.get("type") == "review" and review_clip is None:
                    review_clip = clip
            if not (delivery_clip and review_clip):
                continue
            options.append(
                {
                    "video": video,
                    "delivery": delivery,
                    "delivery_clip": delivery_clip,
                    "review_clip": review_clip,
                    "youtube_url": youtube_url,
                }
            )
    return options


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Unable to locate data file at {DATA_PATH}")

    with DATA_PATH.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    deliveries = _collect_deliveries(data)
    if not deliveries:
        raise RuntimeError("No valid deliveries with both delivery and review clips were found.")

    selection = random.choice(deliveries)
    delivery_info = selection["delivery"]
    delivery_clip = selection["delivery_clip"]
    review_clip = selection["review_clip"]
    youtube_url = selection["youtube_url"]

    delivery_link = _build_link(youtube_url, delivery_clip["start"])
    review_link = _build_link(youtube_url, review_clip["start"])

    match = selection["video"].get("match", {})
    teams = match.get("teams", ["?", "?"])
    match_desc = f"{teams[0]} vs {teams[1]}" if len(teams) == 2 else "Unknown teams"

    print("Random LBW delivery")
    print("-------------------")
    print(f"Match: {match_desc}")
    venue = match.get("venue")
    if venue:
        print(f"Venue: {venue}")
    match_date = match.get("match_date")
    if match_date:
        print(f"Date: {match_date}")
    print(
        f"Scenario: Inn {delivery_info.get('innings')} | Over {delivery_info.get('over')}"
        f" | Ball {delivery_info.get('ball')}"
    )
    print(
        f"Players: {delivery_info.get('bowler')} to {delivery_info.get('batter')}"
    )
    print()
    print(f"Delivery clip: {delivery_link}")
    print(f"Review clip:   {review_link}")


if __name__ == "__main__":
    main()
