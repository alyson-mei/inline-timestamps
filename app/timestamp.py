from enum import Enum
from datetime import datetime, time


class TimestampFormat(Enum):
    """Supported time string formats."""

    FULL = "%H:%M:%S"
    SHORT = "%H:%M"

    def to_regex(self) -> str:
        """Return a regex pattern matching this format."""

        match self:
            case TimestampFormat.SHORT:
                return r"\d{2}:\d{2}(?!:\d{2})"
            case TimestampFormat.FULL:
                return r"\d{2}:\d{2}:\d{2}"

    @classmethod
    def combined_regex(cls) -> str:
        """Return a regex matching either format, full takes priority."""

        full = cls.FULL.to_regex()
        short = cls.SHORT.to_regex()
        return rf"(?:{full}|{short})"


class Timestamp:
    """Wrapper around datetime.time with parsing support."""

    def __init__(
        self,
        timestamp: "Timestamp" | datetime | time | str,
        ts_format: TimestampFormat = TimestampFormat.FULL,
    ):
        """Initialize from time, datetime, string, or Timestamp."""
        self.value = None
        self.format = ts_format

        if isinstance(timestamp, Timestamp):
            self.value = timestamp.value
            return

        if isinstance(timestamp, time):
            self.value = timestamp
            return

        if isinstance(timestamp, datetime):
            self.value = timestamp.time()
            return

        if isinstance(timestamp, str):
            try:
                self.value = datetime.strptime(
                    timestamp,
                    self.format.value
                ).time()
                return

            except ValueError:
                for ts_fmt in TimestampFormat:
                    try:
                        self.value = datetime.strptime(
                            timestamp,
                            ts_fmt.value
                        ).time()
                        return

                    except ValueError:
                        pass

                raise ValueError(
                    f"Invalid timestamp string: {timestamp}"
                )

        raise TypeError(
            "Timestamp must be time, datetime, str, or Timestamp"
        )

    def __str__(self):
        """Return the timestamp formatted as a string."""

        return self.value.strftime(self.format.value)

    def __repr__(self):
        """Return a debug representation."""

        return f"Timestamp({self.value!r})"

    def __eq__(self, other):
        """Compare timestamps by time value."""

        if isinstance(other, Timestamp):
            return self.value == other.value
        return False

    def __sub__(self, other):
        """
        Subtract another Timestamp from a given one.
        """

        if isinstance(other, Timestamp):
            today = datetime.today().date()
            dt1 = datetime.combine(today, self.value)
            dt2 = datetime.combine(today, other.value)
            return (dt1 - dt2).total_seconds()
        raise TypeError("Subtraction only supported between Timestamps")