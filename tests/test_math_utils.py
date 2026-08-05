import pytest

from math_utils import add, divide, multiply, subtract


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6


def test_divide():
    assert divide(10, 2) == 5
    assert divide(1, 4) == 0.25


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(1, 0)
