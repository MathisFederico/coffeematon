from coffeematon.__main__ import experiment_for_n


def test_int():
    experiment_for_n("int", 10)


def test_nonint():
    experiment_for_n("nonint", 10)


def test_int_circular():
    experiment_for_n("int", 10, init="circular")


def test_nonint_circular():
    experiment_for_n("nonint", 10, init="circular")
