from coffeematon.coarse_grain import grain_coords

import numpy as np


class TestGrain:
    def test_grain_3_middle_odd(self):
        """
        |0|1|2|3|4|     |0|1|2|3|4|
        |1|_|_|_|_|     |1|x|x|x|_|
        |2|_|x|_|_| =>  |2|x|x|x|_|
        |3|_|_|_|_|     |3|x|x|x|_|
        |4|_|_|_|_|     |4|_|_|_|_|
        """
        assert grain_coords(2, 2, 3, 4, 4) == (1, 3, 1, 3)

    def test_grain_3_middle_even(self):
        """
        |0|1|2|3|4|     |0|1|2|3|4|
        |1|_|_|_|_|     |1|_|_|_|_|
        |2|_|_|_|_| =>  |2|_|x|x|x|
        |3|_|_|x|_|     |3|_|x|x|x|
        |4|_|_|_|_|     |4|_|x|x|x|
        """
        assert grain_coords(3, 3, 3, 4, 4) == (2, 4, 2, 4)

    def test_grain_3_min_corner(self):
        """
        |0|1|2|3|4|     |x|x|x|3|4|
        |1|x|_|_|_|     |x|x|x|_|_|
        |2|_|_|_|_| =>  |x|x|x|_|_|
        |3|_|_|_|_|     |3|_|_|_|_|
        |4|_|_|_|_|     |4|_|_|_|_|
        """
        assert grain_coords(0, 0, 3, 4, 4) == (0, 1, 0, 1)

    def test_grain_3_max_corner(self):
        """
        |0|1|2|3|4|     |0|1|2|3|4|
        |1|_|_|_|_|     |1|_|_|_|_|
        |2|_|_|_|_| =>  |2|_|_|_|_|
        |3|_|_|_|_|     |3|_|_|x|x|
        |4|_|_|_|x|     |4|_|_|x|x|
        """
        assert grain_coords(4, 4, 3, 4, 4) == (3, 4, 3, 4)
