from lib.sample import Math


def test_sum():
    result = Math.sum(2, 2)
    assert result == 4


def test_mul():
    result = Math.mul(2, 2)
    assert result == 4
