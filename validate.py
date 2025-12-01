import json
import sys
from collections import Counter
from jsonschema import ValidationError, validate


def _parse_timestamp(ts: str) -> int:
    parts = ts.split(":")
    if len(parts) != 3:
        raise ValueError(f"Timestamp must be HH:MM:SS, got {ts}")
    hours, minutes, seconds = map(int, parts)
    return hours * 3600 + minutes * 60 + seconds


def _format_duration(seconds: float) -> str:
    total_seconds = int(round(seconds))
    mm, ss = divmod(total_seconds, 60)
    hh, mm = divmod(mm, 60)
    if hh:
        return f"{hh:d}h {mm:02d}m {ss:02d}s"
    if mm:
        return f"{mm:d}m {ss:02d}s"
    return f"{ss:d}s"


def _compute_metrics(data: dict) -> dict:
    videos = data.get("videos", [])
    delivery_count = 0
    clip_lengths = {"delivery": [], "review": []}
    format_counter: Counter[str] = Counter()

    for video in videos:
        match_info = video.get("match", {})
        format_name = match_info.get("format")

        for delivery in video.get("deliveries", []):
            delivery_count += 1
            if format_name:
                format_counter[format_name] += 1
            for clip in delivery.get("clips", []):
                clip_type = clip.get("type")
                if clip_type not in clip_lengths:
                    continue
                try:
                    duration = _parse_timestamp(clip["end"]) - _parse_timestamp(clip["start"])
                except (ValueError, KeyError):
                    continue
                if duration >= 0:
                    clip_lengths[clip_type].append(duration)

    metrics = {
        "video_count": len(videos),
        "delivery_count": delivery_count,
        "format_counts": format_counter,
        "avg_clip_lengths": {},
    }

    for clip_type, durations in clip_lengths.items():
        avg = sum(durations) / len(durations) if durations else 0
        metrics["avg_clip_lengths"][clip_type] = avg

    return metrics


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate.py <datafile.json>")
        sys.exit(1)

    data_path = sys.argv[1]
    schema_path = "lbw_schema.json"

    try:
        with open(schema_path, "r") as f:
            schema = json.load(f)
    except FileNotFoundError:
        print(f"Schema file not found: {schema_path}")
        sys.exit(1)

    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Data file not found: {data_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in data file: {e}")
        sys.exit(1)

    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        print("Validation error:")
        print(e.message)
        print("\nLocation:", list(e.path))
        sys.exit(1)

    metrics = _compute_metrics(data)
    print("Valid!\n")
    print(f"Videos: {metrics['video_count']}")
    print(f"Deliveries: {metrics['delivery_count']}")

    if metrics["format_counts"]:
        print("Deliveries per format:")
        for fmt, count in metrics["format_counts"].most_common():
            print(f"  {fmt}: {count}")

    avg_delivery = metrics["avg_clip_lengths"].get("delivery", 0)
    avg_review = metrics["avg_clip_lengths"].get("review", 0)
    print("Average clip lengths:")
    print(f"  Delivery: {_format_duration(avg_delivery)}")
    print(f"  Review:   {_format_duration(avg_review)}")


if __name__ == "__main__":
    main()
