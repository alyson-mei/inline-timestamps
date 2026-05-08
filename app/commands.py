import re
from enum import Enum
from app.timestamp import Timestamp, TimestampFormat


class Commands(Enum):
    TS = r"\ts"
    TD = r"\td"
    OPEN = r"\open"
    CLOSE = r"\open" + "\\"

    @classmethod
    def pattern(cls) -> str:
        _ts = TimestampFormat.combined_regex()
        full_open = rf"(?P<open_start>{_ts}) -> {_ts} {re.escape(cls.OPEN.value)}(?!\\)"
        full_close = rf"(?P<close_start>{_ts}) -> {_ts} {re.escape(cls.CLOSE.value)}"
        return "|".join([
            full_close,
            full_open,
            re.escape(cls.TS.value),
            re.escape(cls.TD.value),
        ])


def replacer(match: re.Match, timestamp: Timestamp) -> str:
    _ts = TimestampFormat.combined_regex()
    full_open = rf"(?P<open_start>{_ts}) -> {_ts} {re.escape(Commands.OPEN.value)}(?!\\)"
    full_close = rf"(?P<close_start>{_ts}) -> {_ts} {re.escape(Commands.CLOSE.value)}"
    command = match.group(0)

    if command == Commands.TS.value:
        return str(timestamp)
    elif command == Commands.TD.value:
        return f"{timestamp} -> {timestamp} {Commands.OPEN.value}"
    elif re.match(full_close, command):
        start = match.group("close_start")
        return f"{start} -> {timestamp}"
    elif re.match(full_open, command):
        start = match.group("open_start")
        return f"{start} -> {timestamp} {Commands.OPEN.value}"
    return command