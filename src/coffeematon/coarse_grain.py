"""Coarse-graining algorithm"""

import numpy as np
from scipy.ndimage import uniform_filter


def smooth(fine: np.ndarray, grainsize: int):
    return uniform_filter(fine, size=grainsize, mode="nearest")


def coarse_grained(smoothed: np.ndarray, maxval: int, n_categories: int = 3):
    maxval = max(maxval, np.max(smoothed))
    bin_size = maxval / (n_categories - 1)
    bins = np.linspace(
        start=-bin_size / 2,
        stop=maxval + bin_size / 2,
        num=n_categories + 1,
        endpoint=True,
    )
    digitized_rounded = bins[np.digitize(smoothed, bins, right=True)] - bin_size / 2
    return digitized_rounded
