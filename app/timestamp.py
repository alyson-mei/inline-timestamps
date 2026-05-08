from enum import Enum
from datetime import datetime, time
from typing import Union


class TimestampFormat(Enum):
    """Supported string formats for Timestamp."""

    FULL = "%H:%M:%S"
    SHORT = "%H:%M"


class Timestamp:
    """Wrapper around datetime.time with parsing support."""

    def __init__(
        self,
        timestamp: Union["Timestamp", datetime, time, str],
        ts_format: TimestampFormat = TimestampFormat.FULL,
    ):
        """
        Initialize from time, datetime, string, or Timestamp.
        """
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