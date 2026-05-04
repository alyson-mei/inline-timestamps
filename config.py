from pathlib import Path
from app.timestamp import Format

DEBOUNCE_TIME = 0.3
TS_FORMAT = Format.SHORT

def _fmt_to_regex(fmt: Format) -> str:
    match fmt:
        case Format.SHORT:
            return r"\d{2}:\d{2}(?!:\d{2})"
        case Format.FULL:
            return r"\d{2}:\d{2}:\d{2}"

_reg = _fmt_to_regex(TS_FORMAT)

ts_regex = r"\\ts"
ts_double_regex = rf"{_reg} -> {_reg}"

# === For development only ===

test_file_path = Path("tests/test_file.md")
test_file_path.touch(exist_ok=True)
