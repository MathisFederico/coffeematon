"""Diff-based encoding"""


def generate_diff(fine, coarse):
    """Generate a diff between the fine-grained and coarse-grained arrays:
    - A value of 0.5 indicates that the arrays are identical.
    - A value of 0 or 1 indicates the correct value in the fine-grained array.
    """
    n = len(fine)
    diff = fine
    for x in range(n):
        for y in range(n):
            if fine[y][x] == coarse[y][x]:
                diff[y][x] = 0.5
    return diff
