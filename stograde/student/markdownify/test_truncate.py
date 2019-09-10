import pytest
from .truncate import truncate


def test_truncate():
    assert truncate("a long string", 5) == "a lon"
    assert truncate("a", 5) == "a"

    assert truncate("😀😀😀", 4) == "😀"
    assert truncate("😀😀😀", 8) == "😀😀"
    assert truncate("😀😀😀", 12) == "😀😀😀"

    assert truncate("абвгд", 5) == "аб"

    try:
        truncate("😀😀😀", 1)
    except UnicodeDecodeError:
        pytest.fail("Unexpected UnicodeDecodeError")

    assert truncate("👨‍👨‍👧‍👧", 4) == "👨"
    assert truncate("👨‍👨‍👧‍👧", 7) == "👨‍"
