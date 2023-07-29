import os
import shutil
import numpy as np
import random
from enum import Enum
from pathlib import Path
from typing import Optional

from abc import abstractmethod

from tqdm import trange

from coffeematon.coarse_grain import coarse_grained, adjusted_coarse_grained
from coffeematon.diff_encoding import generate_diff
from coffeematon.encoding import zip_array, save_image
from coffeematon.mdl import encoded_sizes


class Complexities(Enum):
    ENTROPY = "entropy"
    COARSE = "coarse"
    ADJ_COARSE = "adj_coarse"
    DIFF = "diff"
    # MDL_COMPLEXITY = "mdlc"
    # MDL_ENTROPY = "mdle"


class InitialStates(Enum):
    UPDOWN = "updown"
    CIRCULAR = "circular"


class Automaton:
    NAME = "GENERIC"

    def __init__(self, n, initial_state: Optional[InitialStates] = None):
        self.n = n
        if initial_state is None:
            initial_state = InitialStates.UPDOWN

        self.initial_state = InitialStates(initial_state)
        self.cells = np.zeros((n, n))
        self.step = 0
        self.steps = []
        self.complexities = {complexity: [] for complexity in Complexities}
        self.esttime = self.timesteps()
        self.dir = Path("experiments") / self.initial_state.value / self.NAME / str(n)
        # Compute grain size
        grainsize = round(0.2 * n)
        if grainsize % 2 == 0:
            grainsize += 1
        self.grainsize = grainsize
        # Set max value for coarse-grained image thresholding
        self.maxval = 1.0

    def set_initial_state(self):
        if self.initial_state is InitialStates.UPDOWN:
            self.cells[: self.n // 2, : self.n] = self.maxval
        elif self.initial_state is InitialStates.CIRCULAR:
            for x in range(self.n):
                for y in range(self.n):
                    if (
                        np.sqrt((x - self.n / 2) ** 2 + (y - self.n / 2) ** 2)
                        < self.n / 4
                    ):
                        self.cells[x, y] = self.maxval

    @abstractmethod
    def next(self):
        """Move the automaton one state ahead by switching two cells."""

    @abstractmethod
    def timesteps(self):
        """Return the estimated number of steps to convergence for the automaton."""

    def simulate(self):
        """Simulate the automaton until convergence is reached."""
        self.set_initial_state()
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)
        os.makedirs(self.dir)
        n_steps = self.esttime
        loadbar = trange(n_steps, total=n_steps, desc="Simulating")
        for step in loadbar:
            stepsize = n_steps // 1000
            if (stepsize == 0) or (step % stepsize) == 0:
                coarse = coarse_grained(self.cells, self.maxval, self.grainsize)
                adj_coarse = adjusted_coarse_grained(
                    self.cells, self.maxval, self.grainsize
                )
                diff_cells = generate_diff(self.cells, coarse)

                self.steps.append(step)
                self.compute_complexities(coarse, adj_coarse, diff_cells)

                # Loadbar display
                loadbar.desc = " | ".join(
                    ["Simulating"]
                    + [
                        f"{c_type.value.capitalize()}: {c_vals[-1]:.2E}"
                        for c_type, c_vals in self.complexities.items()
                    ]
                )
                loadbar.update()

                # Bitmap images
                self.save_images(step, coarse, adj_coarse, diff_cells)

            self.step = step
            self.next()

    def compute_complexities(self, coarse, adj_coarse, diff_cells):
        entropy = zip_array(self.cells)
        self.complexities[Complexities.ENTROPY].append(entropy)

        coarse_complexity = zip_array(coarse)
        self.complexities[Complexities.COARSE].append(coarse_complexity)

        adj_coarse_complexity = zip_array(adj_coarse)
        self.complexities[Complexities.ADJ_COARSE].append(adj_coarse_complexity)

        diff_complexity = zip_array(diff_cells)
        self.complexities[Complexities.DIFF].append(diff_complexity)

        # mdl_complexity, mdl_entropy = encoded_sizes(self.cells)
        # self.complexities[Complexities.MDL_COMPLEXITY].append(mdl_complexity)
        # self.complexities[Complexities.MDL_ENTROPY].append(mdl_entropy)

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
