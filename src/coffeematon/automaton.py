import os
import numpy as np
import random

from coffeematon.coarse_grain import coarse_grained, adjusted_coarse_grained, ACG_V
from coffeematon.diff_encoding import generate_diff
from coffeematon.encoding import zip_array, save_image
from coffeematon.mdl import encoded_sizes


metrics = {
    "cg": "Coarse-Grained",
    "mdl": "MDL Compressed",
    "diff": "Diff Compressed",
    "acg": "Adjusted Coarse-Grained",
}


class Automaton:
    def __init__(self, n, metric):
        self.cells = np.concatenate(
            [np.ones((n // 2, n)), np.zeros((n // 2, n))], axis=0
        )
        self.n = n
        self.i = 0
        self.x = []
        self.entropies = []
        self.complexities = []
        self.esttime = self.timesteps()
        self.dir = "int_%s_%d" % (metric, n)
        # Check that requested metric exists, then set it
        if metric in metrics:
            self.metric = metric
        else:
            print("Unknown metric")
            exit()
        # Compute grain size
        grainsize = round(n**0.5)
        if grainsize % 2 == 0:
            grainsize -= 1
        self.grainsize = grainsize
        # Set max value for coarse-grained image thresholding
        self.maxval = 1.0

    def simulate(self):
        """Simulate the automaton until convergence is reached."""
        os.mkdir(self.dir)
        while not self.mixed():
            stepsize = self.esttime / 400
            if (stepsize == 0) or (self.i % (self.esttime / 400)) == 0:
                (complexity, entropy) = self.compressed_sizes()
                self.x.append(self.i)
                self.entropies.append(entropy)
                self.complexities.append(complexity)
            self.next()

    def mixed(self):
        """Test whether convergence has been reached."""
        if self.i > self.esttime * 4:
            return True
        else:
            return False
        # if (len(self.complexities) < 10):
        #    return False
        # else:
        #    recent = self.complexities[-10:]
        #    return max(recent)-min(recent) < 3

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
            self.next()
        else:
            self.cells[y0][x0], self.cells[y1][x1] = (
                self.cells[y1][x1],
                self.cells[y0][x0],
            )
            self.i += 1

    def compressed_sizes(self):
        """Return a tuple (complexity, entropy) for the current state of the automaton,
        estimated using the chosen metric."""
        if self.metric == "cg":
            coarse = coarse_grained(self.cells, self.maxval, self.grainsize)
            complexity = zip_array(coarse)
            entropy = zip_array(self.cells)
            # Save images
            save_image(self.cells, self.dir + "/fine_" + str(self.i) + ".bmp", self.n)
            save_image(coarse, self.dir + "/coarse_" + str(self.i) + ".bmp", self.n)
            return (complexity, entropy)
        if self.metric == "mdl":
            (complexity, entropy) = encoded_sizes(self.cells)
            # Save images
            save_image(self.cells, self.dir + "/fine_" + str(self.i) + ".bmp", self.n)
            return (complexity, entropy)
        if self.metric == "diff":
            coarse = coarse_grained(self.cells, self.maxval, self.grainsize)
            diff_cells = generate_diff(self.cells, coarse)
            complexity = zip_array(coarse)
            entropy = complexity + zip_array(diff_cells)
            # Save images
            save_image(self.cells, self.dir + "/fine_" + str(self.i) + ".bmp", self.n)
            save_image(coarse, self.dir + "/coarse_" + str(self.i) + ".bmp", self.n)
            save_image(diff_cells, self.dir + "/diff_" + str(self.i) + ".bmp", self.n)
            return (complexity, entropy)
        if self.metric == "acg":
            coarse = coarse_grained(self.cells, self.maxval, self.grainsize, v=ACG_V)
            adj_coarse = adjusted_coarse_grained(
                self.cells, self.maxval, self.grainsize
            )
            complexity = zip_array(adj_coarse)
            entropy = zip_array(self.cells)
            # Save images
            save_image(self.cells, self.dir + "/fine_" + str(self.i) + ".bmp", self.n)
            save_image(coarse, self.dir + "/coarse_" + str(self.i) + ".bmp", self.n)
            save_image(
                adj_coarse, self.dir + "/adj_coarse_" + str(self.i) + ".bmp", self.n
            )
            return (complexity, entropy)

    def timesteps(self):
        """Return the estimated number of steps to convergence for the automaton."""
        if self.n < 30:
            return 25000
        return 2495 * (self.n**2) - 173600 * self.n + 3029000
