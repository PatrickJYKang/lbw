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


def _collect_clips(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    options: List[Dict[str, Any]] = []
    for video in data.get("videos", []):
        youtube_url = video.get("youtube_url")
        if not youtube_url:
            continue
        for delivery in video.get("deliveries", []):
            for clip in delivery.get("clips", []):
                clip_type = clip.get("type")
                if clip_type not in {"delivery", "review"}:
                    continue
                start = clip.get("start")
                end = clip.get("end")
                if not (start and end):
                    continue
                options.append(
                    {
                        "video": video,
                        "delivery": delivery,
                        "clip": clip,
                        "youtube_url": youtube_url,
                    }
                )
    return options


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Unable to locate data file at {DATA_PATH}")

    with DATA_PATH.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    clips = _collect_clips(data)
    if not clips:
        raise RuntimeError("No valid clips with both start and end times were found.")

    selection = random.choice(clips)
    delivery_info = selection["delivery"]
    clip = selection["clip"]
    youtube_url = selection["youtube_url"]

    clip_link = _build_link(youtube_url, clip["start"])

    match = selection["video"].get("match", {})
    teams = match.get("teams", ["?", "?"])
    match_desc = f"{teams[0]} vs {teams[1]}" if len(teams) == 2 else "Unknown teams"

    result = {
        "video_id": selection["video"].get("id"),
        "youtube_url": youtube_url,
        "match": {
            "description": match_desc,
            "teams": match.get("teams"),
            "venue": match.get("venue"),
            "format": match.get("format"),
            "match_date": match.get("match_date"),
            "year": match.get("year"),
        },
        "delivery": {
            "id": delivery_info.get("id"),
            "innings": delivery_info.get("innings"),
            "over": delivery_info.get("over"),
            "ball": delivery_info.get("ball"),
            "team_bowling": delivery_info.get("team_bowling"),
            "team_batting": delivery_info.get("team_batting"),
            "bowler": delivery_info.get("bowler"),
            "batter": delivery_info.get("batter"),
            "onfield_decision": delivery_info.get("onfield_decision"),
            "final_decision": delivery_info.get("final_decision"),
            "drs": delivery_info.get("drs"),
        },
        "clip": {
            "type": clip.get("type"),
            "start": clip.get("start"),
            "end": clip.get("end"),
            "link": clip_link,
            "tag": clip.get("tag"),
            "notes": clip.get("notes"),
        },
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
