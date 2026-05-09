import yaml
from pathlib import Path
from app.timestamp import TimestampFormat


def _load() -> dict:
    return yaml.safe_load(Path("config.yaml").read_text())


def _fmt_to_regex(fmt: TimestampFormat) -> str:
    match fmt:
        case TimestampFormat.SHORT:
            return r"\d{2}:\d{2}(?!:\d{2})"
        case TimestampFormat.FULL:
            return r"\d{2}:\d{2}:\d{2}"


_cfg = _load()
DEBOUNCE_TIME = 0.3
SELF_WRITE_GUARD = 0.5
STATS_SEPARATOR = _cfg["stats_separator"]
TS_FORMAT = TimestampFormat[_cfg["ts_format"]]


_short = _fmt_to_regex(TimestampFormat.SHORT)
_full = _fmt_to_regex(TimestampFormat.FULL)

ts_regex = r"\\ts"
ts_double_regex = rf"({_full}|{_short}) -> ({_full}|{_short})"

# === For development only ===

FILE_PATH = Path(_cfg["file_path"])
FILE_PATH.touch(exist_ok=True)
