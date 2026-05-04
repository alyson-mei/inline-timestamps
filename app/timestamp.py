from enum import Enum
from datetime import datetime, time

class Format(Enum):
    FULL = "%H:%M:%S"
    SHORT = "%H:%M"

class Timestamp:
    def __init__(self, timestamp, fmt=Format.FULL):
        self.format = fmt

        if isinstance(timestamp, datetime):
            self.value = timestamp.time()
            return

        if isinstance(timestamp, time):
            self.value = timestamp
            return

        if isinstance(timestamp, str):
            for ts_fmt in Format:
                try:
                    self.value = datetime.strptime(timestamp, ts_fmt.value).time()
                    return
                except ValueError:
                    pass

        raise TypeError("Timestamp must be datetime, time, or str")

    def __str__(self):
        return self.value.strftime(self.format.value)

    def __repr__(self):
        return f"Timestamp({self.value!r})"

    def __eq__(self, other):
        if isinstance(other, Timestamp):
            return self.value == other.value
        return False
