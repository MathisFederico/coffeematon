"""Coarse-graining algorithm"""

import numpy
from typing import Tuple

ACG_V = 7


def coarse_grained(fine, maxval, grainsize, n_categories=3):
    n = len(fine)
    result = numpy.zeros((n, n))
    for x in range(n):
        for y in range(n):
            result[y][x] = threshold(
                average(grain(fine, x, y, grainsize)), n_categories, maxval
            )
    return result


def threshold(value, n_categories, maxval):
    """Threshold a floating-point value into one of v values."""
    # Normalize value
    norm_val = value / maxval
    # Threshold into 3 different-size buckets for coarse-graining
    if n_categories == 3:
        if value <= 1.0 / 3.0:
            return 0.0
        elif value <= 2.0 / 3.0:
            return 0.5
        else:
            return 1
    # Threshold into v evenly-sized buckets for adjusted coarse-graining
    else:
        thresholds = numpy.linspace(0, 1, n_categories)
        for threshold in thresholds:
            if norm_val <= threshold:
                return threshold
        return 1


def grain_coords(
    x: int, y: int, grainsize: int, x_lim: int, y_lim: int
) -> Tuple[int, int, int, int]:
    xmin = max(0, x - grainsize // 2)
    xmax = min(x_lim, x + grainsize // 2)
    ymin = max(0, y - grainsize // 2)
    ymax = min(y_lim, y + grainsize // 2)
    return xmin, xmax, ymin, ymax


def grain(array, x, y, grainsize):
    """Return the grainsize x grainsize block centered around index (x, y)."""
    xmin, xmax, ymin, ymax = grain_coords(x, y, grainsize, len(array), len(array[0]))
    return array[ymin:ymax, xmin:xmax]


def average(array):
    """Return the average of values in a 2-dimensional array."""
    total = numpy.sum(array)
    return total / float(len(array) * len(array[0]))


def adjusted_coarse_grained(fine, maxval, grainsize):
    """Adjusted coarse-graining"""
    n = len(fine)
    coarse = coarse_grained(fine, maxval, grainsize, n_categories=ACG_V)
    adjusted = numpy.zeros((n, n))
    thresholds = numpy.linspace(0, 1, ACG_V)
    stepsize = thresholds[1] - thresholds[0]
    for y in range(n):
        maj = majority(coarse[y])
        diff = max(coarse[y]) - min(coarse[y])
        if diff <= (1.1 * stepsize):  # Correct for floating point error
            adjusted[y] = [maj] * n
        else:
            adjusted[y] = coarse[y]
    return adjusted


def majority(list):
    counts = {}
    for item in list:
        counts[item] = counts.get(item, 0) + 1
    max_freq = max(counts.values())
    for item in counts:
        if counts[item] == max_freq:
            return item
