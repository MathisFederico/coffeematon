from pathlib import Path

import numpy as np
import random

from coffeematon.automaton import Automaton


class NonInteractingAutomaton(Automaton):
    def __init__(self, n, metric):
        Automaton.__init__(self, n, metric)
        self.maxval = self.grainsize
        if metric == "acg":
            self.maxval = int(self.grainsize**0.5)
        self.dir = Path("experiments") / "nonint" / str(n) / str(metric)
        self.esttime *= 2

    # Move the automaton one state ahead by switching two cells.
    def next(self):
        new_cells = np.zeros((self.n, self.n))
        for x0 in range(self.n):
            for y0 in range(self.n):
                for i in range(int(self.cells[y0][x0])):
                    # Randomly pick a direction to move
                    xd = 0
                    yd = 0
                    direction = random.randrange(0, 4)
                    if direction == 0:
                        xd = -1
                    if direction == 1:
                        xd = 1
                    if direction == 2:
                        yd = -1
                    if direction == 3:
                        yd = 1
                    # Insert particle into new cell
                    x1 = max(0, min(self.n - 1, x0 + xd))
                    y1 = max(0, min(self.n - 1, y0 + yd))
                    new_cells[y1][x1] += 1
        self.cells = new_cells

    # Return the estimated number of steps to convergence
    # for the automaton.
    def timesteps(self):
        return self.n**2 / 4
