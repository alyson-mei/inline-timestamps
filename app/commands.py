import re
from enum import Enum
from app.timestamp import Timestamp, TimestampFormat


class Commands(Enum):
    TS = r"\ts"
    TD = r"\td"
    TI = r"\ti"
    OPEN_SW = r"\stopwatch"
    CLOSE_SW = r"\stopwatch" + "\\"

    @classmethod
    def pattern(cls) -> str:
        _ts = re.escape(cls.TS.value)
        _open = re.escape(cls.OPEN_SW.value)
        _close = re.escape(cls.CLOSE_SW.value)
        return "|".join([
            rf"{_ts}\s+{_close}",
            rf"{_ts}\s+{_open}(?!\\)",
            rf"{_ts}(?!\s+{_open})",
            re.escape(cls.TD.value),
            re.escape(cls.TI.value),
        ])


def replacer(match: re.Match, timestamp: Timestamp) -> str:
    _ts = re.escape(Commands.TS.value)
    _open = re.escape(Commands.OPEN_SW.value)
    _close = re.escape(Commands.CLOSE_SW.value)
    command = match.group(0)

    if re.match(rf"{_ts}\s+{_close}", command):
        return str(timestamp)
    elif re.match(rf"{_ts}\s+{_open}(?!\\)", command):
        return command
    elif command == Commands.TD.value:
        return f"{timestamp} -> {Commands.TS.value} {Commands.OPEN_SW.value}"
    elif command == Commands.TI.value:
        return f"{timestamp} -> {Commands.TS.value}"
    else:
        return str(timestamp)