from coffeematon.mdl import substring_counts, scr, substrings


def test_substring_counts():
    x = ["010101"]
    c = substring_counts(x, 1, 3)
    assert c["01"] == 3
    assert c["010"] == 1


def test_scr_00():
    """test for score for symbol '00' in string '00110011'"""
    assert scr("00", 2, 8) == 1


def test_scr_001():
    """test for symbol '001' in string '0011001001000010100101001100100110011001'"""
    assert scr("001", 10, 40) - 0.4333 <= 0.001


def test_substrings():
    x = "abcdef"
    assert len(substrings(x, 2)) == 5
