import re
from pathlib import Path
from datetime import datetime, date
from app.timestamp import Timestamp
from config import ts_double_regex

def _to_timestamp(val) -> Timestamp:
    if isinstance(val, Timestamp):
        return val
    if isinstance(val, str):
        return Timestamp(val)
    raise TypeError(f"cannot convert {type(val)} to Timestamp")

def _delta_minutes(start, end) -> int:
    d = date.today()
    s = datetime.combine(d, _to_timestamp(start).value)
    e = datetime.combine(d, _to_timestamp(end).value)
    return int((e - s).total_seconds() // 60)

def _parse_category(line: str) -> str | None:
    stripped = line.strip()
    match = re.match(r"^(\w[\w\s]*):\s*$", stripped)
    if match:
        return match.group(1).strip()
    return None

def compute_stats(file_path: Path) -> dict[str, int]:
    lines = file_path.read_text().splitlines()
    stats: dict[str, int] = {}
    prev_non_empty = None

    for line in lines:
        if not line.strip():
            continue

        match = re.search(ts_double_regex, line)
        if match:
            start, end = match.group(0).split(" -> ")
            delta = _delta_minutes(start, end)

            category = ""
            if prev_non_empty is not None:
                current_indent = len(line) - len(line.lstrip())
                prev_indent = len(prev_non_empty) - len(prev_non_empty.lstrip())
                candidate = _parse_category(prev_non_empty)
                if candidate is not None and current_indent > prev_indent:
                    category = candidate

            stats[category] = stats.get(category, 0) + delta

        prev_non_empty = line

    return stats

def _format_min(minutes: int) -> str:
    if minutes >= 60:
        return f"{minutes // 60} hrs {minutes % 60} min"
    return f"{minutes} min"

def format_stats(stats: dict, indent: int = 4) -> str:
    total = sum(stats.values())
    pad = " " * indent
    start_lines = ["---", f"Total: {_format_min(total)}"]
    mid_lines = [f"{pad}- {category}: {_format_min(minutes)}" for category, minutes in stats.items() if category != ""]
    end_line = [f"{pad}- Rest: {_format_min(stats[''])}"] if "" in stats else []

    return "\n".join(start_lines + mid_lines + end_line)
        
if __name__ == "__main__":
    from config import test_file_path
    stats = compute_stats(test_file_path)
    print(format_stats(stats))
