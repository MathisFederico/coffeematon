"""Diff-based encoding"""


import numpy as np


def generate_diff(fine: np.ndarray, coarse: np.ndarray):
    """Generate a diff between the fine-grained and coarse-grained arrays:
    - A value of 0.5 exactly indicates that the arrays are identical.
    - A value between 0 and 1 indicates the correct value in the fine-grained array.
    Fine grained value can be retrieved by:
        fine = coarse + diff @ mask
        where @ is the element_wise multiplication
    """
    diff = fine.copy()
    mask = np.isclose(fine, coarse)
    diff[mask] = 0.5
    return diff, mask
