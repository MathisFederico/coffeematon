"""Diff-based encoding"""

from copy import deepcopy

import numpy as np


def generate_diff(fine: np.ndarray, coarse: np.ndarray):
    """Generate a diff between the fine-grained and coarse-grained arrays:
    - A value of 0.5 indicates that the arrays are identical.
    - A value of 0 or 1 indicates the correct value in the fine-grained array.
    """
    diff = fine.copy()
    diff[fine == coarse] = 0.5
    return diff
