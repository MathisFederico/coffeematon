import numpy as np
import random

from coffeematon.automatons.automaton import Automaton, InitialStates


class NonInteractingAutomaton(Automaton):
    NAME = "Non-Interacting"

    def __init__(self, *args, **kwargs):
        Automaton.__init__(self, *args, **kwargs)
        self.maxval = self.grainsize

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

    def timesteps(self):
        if self.initial_state is InitialStates.UPDOWN:
            return 100 * self.n
        if self.initial_state is InitialStates.CIRCULAR:
            return 100 * self.n
