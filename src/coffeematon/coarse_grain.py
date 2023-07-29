"""Coarse-graining algorithm"""

import numpy as np
from scipy.ndimage import uniform_filter


def coarse_grained(
    fine: np.ndarray, maxval: int, grainsize: int, n_categories: int = 3
):
    maxval = max(maxval, np.max(fine))
    averaged = uniform_filter(fine, size=grainsize, mode="nearest")
    bin_size = round(maxval / (n_categories - 1), 2)
    bins = np.round(
        np.linspace(
            start=-bin_size / 2,
            stop=maxval + bin_size / 2,
            num=n_categories + 1,
            endpoint=True,
        ),
        2,
    )
    digitized_rounded = bins[np.digitize(averaged, bins)] - bin_size / 2
    return digitized_rounded


def adjusted_coarse_grained(fine: np.ndarray, maxval: int, grainsize: int):
    return coarse_grained(fine, maxval, grainsize, n_categories=7)
