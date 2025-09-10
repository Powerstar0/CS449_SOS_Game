import pytest
from calculator import *


def test_add():
    assert (add(2, 3) == 5)


def test_subtract():
    assert (subtract(2, 3) == -1)
