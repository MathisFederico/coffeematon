from coffeematon.coarse_grain import coarse_grained

import numpy as np


def np_check_equal(actual: np.ndarray, expected: np.ndarray):
    assert np.all(
        actual == expected
    ), f"Got:\n{actual}\nDiff:\n{np.abs(actual-expected)}"


class TestGrain:
    def test_grain_3_bins_11(self):
        fine = np.array(
            [
                [0, 1, 0, 0, 1],
                [0, 1, 1, 0, 1],
                [0, 1, 0, 1, 0],
                [1, 0, 1, 1, 1],
                [1, 0, 1, 0, 0],
            ],
            dtype=np.float32,
        )
        coarsed = coarse_grained(fine, maxval=1.0, grainsize=3, n_categories=11)
        expected = np.array(
            [
                [0.3, 0.4, 0.4, 0.4, 0.7],
                [0.3, 0.4, 0.6, 0.4, 0.6],
                [0.4, 0.6, 0.7, 0.7, 0.7],
                [0.6, 0.6, 0.6, 0.6, 0.4],
                [0.7, 0.7, 0.4, 0.6, 0.3],
            ]
        )
        np_check_equal(coarsed, expected)

    def test_grain_3_bins_3(self):
        fine = np.array(
            [
                [0, 1, 0, 0, 1],
                [0, 1, 1, 0, 1],
                [0, 1, 0, 1, 0],
                [1, 0, 1, 1, 1],
                [1, 0, 1, 0, 0],
            ],
            dtype=np.float32,
        )
        coarsed = coarse_grained(fine, maxval=1.0, grainsize=3, n_categories=3)
        expected = 0.5 * np.ones_like(fine)
        np_check_equal(coarsed, expected)

    def test_grain_3_bins_3_ones(self):
        fine = np.ones((5, 5), dtype=np.float32)
        coarsed = coarse_grained(fine, maxval=1.0, grainsize=3, n_categories=3)
        expected = np.ones((5, 5), dtype=np.float32)
        np_check_equal(coarsed, expected)
