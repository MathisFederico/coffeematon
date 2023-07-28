"""Coarse-graining algorithm"""

import numpy

ACG_V = 7


def coarse_grained(fine, maxval, grainsize, v=3):
    n = len(fine)
    result = numpy.zeros((n, n))
    for x in range(n):
        for y in range(n):
            result[y][x] = threshold(average(grain(fine, x, y, grainsize)), v, maxval)
    return result


def threshold(value, v, maxval):
    """Threshold a floating-point value into one of v values."""
    # Normalize value
    norm_val = value / maxval
    # Threshold into 3 different-size buckets for coarse-graining
    if v == 3:
        if value <= 1.0 / 3.0:
            return 0.0
        elif value <= 2.0 / 3.0:
            return 0.5
        else:
            return 1
    # Threshold into v evenly-sized buckets for adjusted coarse-graining
    else:
        thresholds = numpy.linspace(0, 1, v)
        for threshold in thresholds:
            if norm_val <= threshold:
                return threshold
        return 1


def grain(array, x, y, grainsize):
    """Return the grainsize x grainsize block centered around index (x, y)."""
    n = len(array)
    xmin = max(0, x - grainsize / 2)
    xmax = min(n, x + grainsize / 2)
    ymin = max(0, y - grainsize / 2)
    ymax = min(n, y + grainsize / 2)
    return array[ymin : ymax + 1, xmin : xmax + 1]


def average(array):
    """Return the average of values in a 2-dimensional array."""
    total = numpy.sum(array)
    return total / float(len(array) * len(array[0]))


def adjusted_coarse_grained(fine, maxval, grainsize):
    """Adjusted coarse-graining"""
    n = len(fine)
    coarse = coarse_grained(fine, maxval, grainsize, v=ACG_V)
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
