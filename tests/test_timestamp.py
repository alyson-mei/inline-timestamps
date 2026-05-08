from datetime import datetime, time
import pytest

from app.timestamp import Timestamp, TimestampFormat


def test_from_datetime():
    ts = Timestamp(datetime(2025, 1, 1, 12, 30, 15))
    assert str(ts) == "12:30:15"


def test_from_time():
    ts = Timestamp(time(8, 5))
    assert str(ts) == "08:05:00"


def test_from_short_string():
    ts = Timestamp("09:45")
    assert ts.value == time(9, 45)


def test_from_full_string():
    ts = Timestamp("09:45:10")
    assert ts.value == time(9, 45, 10)


def test_short_format():
    ts = Timestamp("09:45:10", TimestampFormat.SHORT)
    assert str(ts) == "09:45"


def test_equality():
    assert Timestamp("10:00") == Timestamp(time(10, 0))


def test_invalid_type():
    with pytest.raises(TypeError):
        Timestamp(123)


def test_invalid_string():
    with pytest.raises(ValueError):
        Timestamp("abc")