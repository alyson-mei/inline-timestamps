import yaml
from pathlib import Path
from app.timestamp import TimestampFormat


def _load() -> dict:
    return yaml.safe_load(Path("config.yaml").read_text())


_cfg = _load()

DEBOUNCE_TIME = 0.3
SELF_WRITE_GUARD = 0.5

STATS_SEPARATOR = _cfg["stats_separator"]
TS_FORMAT = TimestampFormat[_cfg["ts_format"]]
WATCH_PATHS = [{"path": Path(w["path"]), "recursive": w.get("recursive", False)} for w in _cfg["watch"]]
WATCH_SUFFIXES = set(_cfg["suffixes"])

_short = TimestampFormat.SHORT.to_regex()
_full = TimestampFormat.FULL.to_regex()

ts_double_regex = rf"({_full}|{_short}) -> ({_full}|{_short})"