import re

from app.timestamp import Timestamp, TimestampFormat
from config import ts_double_regex, TS_FORMAT


def _parse_category(line: str) -> str | None:
    """
    Extracts a category name from a line of text.

    Matches lines that optionally end with a colon:
        "CategoryName" or "CategoryName:"

    The category may contain letters, digits, underscores,
    spaces, and hyphens.

    Leading whitespace and bullet markers (*, -) are ignored.
    Returns the category name if found, otherwise None.
    """
    stripped = re.sub(r"^[\s\*\-]+", "", line.strip())
    match = re.match(r"^([A-Za-z_][A-Za-z0-9_\s\-]*):?\s*$", stripped)
    if match:
        return match.group(1).strip()
    return None


def compute_stats(content: str) -> dict[str, int]:
    """
    Parse timestamp pairs from content and accumulate durations by category.

    Categories are inferred from the nearest parent label line with less
    indentation. Timestamps without a parent category are grouped under "".
    Markdown headings (#) reset the current category.

    Returns a dict mapping category name to total seconds.
    """

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
            delta = int(Timestamp(end) - Timestamp(start))
            stats[category] = stats.get(category, 0) + delta
        else:
            candidate = _parse_category(line)
            if candidate is not None:
                current_category = candidate
                category_indent = current_indent

    return stats
    

def _format_time(total_seconds: int, ts_format: TimestampFormat = TS_FORMAT) -> str:
    """
    Formats a duration given in seconds into a human-readable string.

    Supports two output modes:
    - SHORT: hours and minutes (seconds are ignored)
    - FULL: hours, minutes, and seconds

    The format is controlled by TimestampFormat.
    """

    match ts_format:
        case TimestampFormat.SHORT:
            total_minutes = total_seconds // 60
            hours = total_minutes // 60
            if hours > 0:
                return f"{hours} hrs {total_minutes % 60} min"
            return f"{total_minutes} min"

        case TimestampFormat.FULL:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            if hours > 0:
                return f"{hours} hrs {minutes} min {seconds} sec"
            elif minutes > 0:
                return f"{minutes} min {seconds} sec"
            return f"{seconds} sec"


def format_stats(stats: dict) -> str:
    """
    Format a stats dict into a human-readable stats block.

    Named categories are listed first, uncategorized time last as "Other".
    Duration formatting follows TS_FORMAT from config.
    """

    total = sum(stats.values())

    lines = [
        "---",
        "# Statistics",
        "",
        f"- Total: {_format_time(total)}",
    ]

    for category, value in stats.items():
        if category == "":
            continue
        lines.append(f"  - {category}: {_format_time(value)}")

    if "" in stats:
        lines.append(f"  - Other: {_format_time(stats[''])}")

    return "\n".join(lines)