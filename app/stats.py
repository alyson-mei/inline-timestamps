import re
from datetime import datetime, date

from app.timestamp import Timestamp, Format
from config import ts_double_regex, TS_FORMAT

def _to_timestamp(val) -> Timestamp:
    if isinstance(val, Timestamp):
        return val
    if isinstance(val, str):
        return Timestamp(val)
    raise TypeError(f"cannot convert {type(val)} to Timestamp")

def _delta_seconds(start, end) -> int:
    d = date.today()
    s = datetime.combine(d, _to_timestamp(start).value)
    e = datetime.combine(d, _to_timestamp(end).value)
    return int((e - s).total_seconds())

def _parse_category(line: str) -> str | None:
    stripped = re.sub(r"^[\s\*\-]+", "", line.strip())
    match = re.match(r"^([A-Za-z_][A-Za-z0-9_\s\-]*):\s*$", stripped)
    if match:
        return match.group(1).strip()
    return None

def compute_stats(content: str) -> dict[str, int]:
    lines = content.splitlines()
    stats: dict[str, int] = {}
    current_category = ""
    category_indent = -1

    for line in lines:
        if not line.strip():
            continue

        if line.startswith("#"):
            current_category = ""
            category_indent = -1
            continue

        current_indent = len(line) - len(line.lstrip())
        match = re.search(ts_double_regex, line)
        if match:
            category = current_category if current_indent > category_indent else ""
            start, end = match.group(0).split(" -> ")
            delta = _delta_seconds(start, end)
            stats[category] = stats.get(category, 0) + delta
        else:
            candidate = _parse_category(line)
            if candidate is not None:
                current_category = candidate
                category_indent = current_indent

    return stats
    
def _format_time(total_seconds: int, fmt: Format = TS_FORMAT) -> str:
    match fmt:
        case Format.SHORT:
            total_minutes = total_seconds // 60
            hours = total_minutes // 60 
            if hours > 0:
                return f"{hours} hrs {total_minutes % 60} min"
            else:
                return f"{total_minutes} min"
        case Format.FULL:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            if hours > 0:
                return f"{hours} hrs {minutes} min {seconds} sec"
            elif minutes > 0:
                return f"{minutes} min {seconds} sec"
            else:
                return f"{seconds} sec"

def format_stats(stats: dict, indent: int = 4) -> str:
    total = sum(stats.values())
    pad = " " * indent
    start_lines = ["---", f"Total: {_format_time(total)}"]
    mid_lines = [f"{pad}- {category}: {_format_time(minutes)}" for category, minutes in stats.items() if category != ""]
    end_line = [f"{pad}- Rest: {_format_time(stats[''])}"] if "" in stats else []

    return "\n".join(start_lines + mid_lines + end_line)
