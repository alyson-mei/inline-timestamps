import yaml
from pathlib import Path
from app.timestamp import Format

DEBOUNCE_TIME = 0.1
SELF_WRITE_GUARD = 0.3
STATS_SEPARATOR = "\n---"
TS_FORMAT = Format.FULL

def _load() -> dict:
    return yaml.safe_load(Path("config.yaml").read_text())

_cfg = _load()
DEBOUNCE_TIME = _cfg["debounce_time"]
SELF_WRITE_GUARD = _cfg["self_write_guard"]
STATS_SEPARATOR = _cfg["stats_separator"]
TS_FORMAT = Format[_cfg["ts_format"]]

def _fmt_to_regex(fmt: Format) -> str:
    match fmt:
        case Format.SHORT:
            return r"\d{2}:\d{2}(?!:\d{2})"
        case Format.FULL:
            return r"\d{2}:\d{2}:\d{2}"

_short = _fmt_to_regex(Format.SHORT)
_full = _fmt_to_regex(Format.FULL)

ts_regex = r"\\ts"
ts_double_regex = rf"({_full}|{_short}) -> ({_full}|{_short})"

# === For development only ===

FILE_PATH = Path(_cfg["file_path"])
FILE_PATH.touch(exist_ok=True)
