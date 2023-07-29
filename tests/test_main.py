from coffeematon.__main__ import data_for_n


def test_int():
    data_for_n("acg", "int", 10)


def test_nonint():
    data_for_n("acg", "nonint", 10)
