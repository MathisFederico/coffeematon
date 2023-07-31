import random

from coffeematon.automatons.automaton import Automaton, InitialStates


class InteractingAutomaton(Automaton):
    NAME = "Interacting"

    def next(self):
        """Move the automaton one state ahead by switching two cells."""
        # Randomly pick a cell to move
        x0 = random.randrange(0, self.n)
        y0 = random.randrange(0, self.n)
        xd = 0
        yd = 0
        # Randomly pick a direction
        direction = random.randrange(0, 4)
        if direction == 0:
            xd = -1
        if direction == 1:
            xd = 1
        if direction == 2:
            yd = -1
        if direction == 3:
            yd = 1
        # Pick again if cells are same, or swap if different
        x1 = max(0, min(self.n - 1, x0 + xd))
        y1 = max(0, min(self.n - 1, y0 + yd))
        if (x0 == x1 and y0 == y1) or (self.cells[y0][x0] == self.cells[y1][x1]):
            return
        self.cells[y0][x0], self.cells[y1][x1] = (
            self.cells[y1][x1],
            self.cells[y0][x0],
        )

    def timesteps(self):
        if self.initial_state is InitialStates.UPDOWN:
            return 4000 * (self.n**2)
        if self.initial_state is InitialStates.CIRCULAR:
            return 4000 * (self.n**2)
