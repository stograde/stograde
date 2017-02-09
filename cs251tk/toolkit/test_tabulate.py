from .tabulate import find_columns


def test_find_columns():
    assert find_columns(10) == "1 2 3 4 5 6 7 8 9 10"
