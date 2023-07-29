import os
import numpy as np
import random
from pathlib import Path

from tqdm import trange

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
        self.step = 0
        self.x = []
        self.entropies = []
        self.complexities = []
        self.esttime = self.timesteps()
        self.dir = Path("experiments") / "int" / str(n) / str(metric)
        # Check that requested metric exists, then set it
        if metric in metrics:
            self.metric = metric
        else:
            print("Unknown metric")
            exit()
        # Compute grain size
        grainsize = round(np.sqrt(n))
        if grainsize % 2 == 0:
            grainsize -= 1
        self.grainsize = grainsize
        # Set max value for coarse-grained image thresholding
        self.maxval = 1.0

    def simulate(self):
        """Simulate the automaton until convergence is reached."""
        os.makedirs(self.dir, exist_ok=True)
        n_steps = int(4 * self.esttime)
        loadbar = trange(n_steps, total=n_steps, desc="Simulating")
        for step in loadbar:
            stepsize = n_steps // 100
            if (stepsize == 0) or (step % stepsize) == 0:
                coarse = coarse_grained(self.cells, self.maxval, self.grainsize)
                adj_coarse = adjusted_coarse_grained(
                    self.cells, self.maxval, self.grainsize
                )
                diff_cells = generate_diff(self.cells, coarse)
                (complexity, entropy) = self.compressed_sizes(
                    coarse, adj_coarse, diff_cells
                )

                self.x.append(step)
                self.entropies.append(entropy)
                self.complexities.append(complexity)
                loadbar.desc = (
                    f"Simulating | Entropy: {entropy:.2E} | Complexity:{complexity:.2E}"
                )
                loadbar.update()
                self.save_images(step, coarse, adj_coarse, diff_cells)
            self.step = step
            self.next()

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

    def compressed_sizes(self, coarse, adj_coarse, diff_cells):
        """Return a tuple (complexity, entropy) for the current state of the automaton,
        estimated using the chosen metric."""

        if self.metric == "mdl":
            (complexity, entropy) = encoded_sizes(self.cells)
        if self.metric == "cg":
            coarse_size = zip_array(coarse)
            cells_size = zip_array(self.cells)
            complexity = coarse_size
            entropy = cells_size
        if self.metric == "diff":
            coarse_size = zip_array(coarse)
            diff_size = zip_array(diff_cells)
            complexity = coarse_size
            entropy = complexity + diff_size
        if self.metric == "acg":
            cells_size = zip_array(self.cells)
            adj_coarse_size = zip_array(adj_coarse)
            complexity = adj_coarse_size
            entropy = cells_size
        return (complexity, entropy)

    def save_images(self, step: int, coarse=None, adj_coarse=None, diff_cells=None):
        bitmaps_dir = self.dir / "bitmaps"
        fine_dir = bitmaps_dir / "fine"
        os.makedirs(fine_dir, exist_ok=True)
        save_image(self.cells, fine_dir / f"{step}.bmp", self.n)
        if coarse is not None:
            coarse_dir = bitmaps_dir / "coarse"
            os.makedirs(coarse_dir, exist_ok=True)
            save_image(coarse, coarse_dir / f"{step}.bmp", self.n)
        if adj_coarse is not None:
            adj_coarse_dir = bitmaps_dir / "adj_coarse"
            os.makedirs(adj_coarse_dir, exist_ok=True)
            save_image(adj_coarse, adj_coarse_dir / f"{step}.bmp", self.n)
        if diff_cells is not None:
            diff_dir = bitmaps_dir / "diff"
            os.makedirs(diff_dir, exist_ok=True)
            save_image(diff_cells, diff_dir / f"{step}.bmp", self.n)

    def timesteps(self):
        """Return the estimated number of steps to convergence for the automaton."""
        return max(2495 * (self.n**2) - 173600 * self.n + 3029000, 100)
