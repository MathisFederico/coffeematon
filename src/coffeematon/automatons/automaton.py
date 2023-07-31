import os
import shutil
import numpy as np
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, List

from abc import abstractmethod
from csv import DictWriter

from tqdm import trange

from coffeematon.coarse_grain import coarse_grained, smooth
from coffeematon.diff_encoding import generate_diff
from coffeematon.encoding import zip_array
from coffeematon.generate_gifs import generate_gif
from PIL import Image


class ArrayTypes(Enum):
    FINE = "fine"
    COARSE_3 = "coarse_3"
    COARSE_7 = "coarse_7"
    COARSE_11 = "coarse_11"
    DIFF_3 = "diff_3"
    DIFF_7 = "diff_7"
    DIFF_11 = "diff_11"
    MASK_3 = "mask_3"
    MASK_7 = "mask_7"
    MASK_11 = "mask_11"
    # MDL_COMPLEXITY = "mdlc"
    # MDL_ENTROPY = "mdle"


class InitialStates(Enum):
    UPDOWN = "updown"
    CIRCULAR = "circular"


class Automaton:
    NAME = "GENERIC"

    def __init__(
        self, n, initial_state: Optional[InitialStates] = None, save: bool = True
    ):
        self.n = n
        if initial_state is None:
            initial_state = InitialStates.UPDOWN

        self.initial_state = InitialStates(initial_state)
        self.cells = np.zeros((n, n))
        self.step = 0
        self.steps = []
        self.complexities = {complexity: [] for complexity in ArrayTypes}
        self.esttime = self.timesteps()
        self.results_dir = Path("data", "results")
        # Compute grain size
        grainsize = round(np.sqrt(n))
        if grainsize % 2 == 0:
            grainsize += 1
        self.grainsize = grainsize
        # Set max value for coarse-grained image thresholding
        self.maxval = 1.0
        self.parameters = (self.initial_state.value, self.NAME, str(self.n))
        self.save = save

    @staticmethod
    def parameters_to_str(parameters: List[str]):
        return "_".join([param.lower() for param in parameters])

    @staticmethod
    def str_to_parameters(parameters_string: str):
        return parameters_string.split("_")

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

    def simulate(
        self, n_steps: Optional[int] = None, max_save_steps: int = 1000
    ) -> Path:
        """Simulate the automaton until convergence is reached."""
        self.set_initial_state()

        if n_steps is None:
            n_steps = self.esttime

        bitmaps_dir = None
        csv_path = None
        if self.save:
            bitmaps_dir = self.create_bitmaps_results_folder()
            csv_path = self.create_csv_results_file()

        loadbar = trange(n_steps, total=n_steps, desc="Simulating")
        for step in loadbar:
            self.step = step
            save_stepsize = n_steps // max_save_steps
            if (save_stepsize == 0) or (step % save_stepsize) == 0:
                smoothed = smooth(self.cells, self.grainsize)
                coarse_3 = coarse_grained(smoothed, self.maxval, 3)
                coarse_7 = coarse_grained(smoothed, self.maxval, 7)
                coarse_11 = coarse_grained(smoothed, self.maxval, 11)

                diff3, mask3 = generate_diff(self.cells, coarse_3)
                diff7, mask7 = generate_diff(self.cells, coarse_7)
                diff11, mask11 = generate_diff(self.cells, coarse_11)

                c_type_to_arr = {
                    ArrayTypes.FINE: self.cells,
                    ArrayTypes.COARSE_3: coarse_3,
                    ArrayTypes.COARSE_7: coarse_7,
                    ArrayTypes.COARSE_11: coarse_11,
                    ArrayTypes.DIFF_3: diff3,
                    ArrayTypes.DIFF_7: diff7,
                    ArrayTypes.DIFF_11: diff11,
                    ArrayTypes.MASK_3: mask3,
                    ArrayTypes.MASK_7: mask7,
                    ArrayTypes.MASK_11: mask11,
                }

                self.steps.append(step)
                self.compute_complexities(c_type_to_arr)
                if self.save:
                    self.save_results(csv_path)
                    self.save_images(bitmaps_dir, step, c_type_to_arr)

                # Loadbar display
                relevant_types = [ArrayTypes.FINE, ArrayTypes.COARSE_3]
                loadbar.desc = " | ".join(
                    ["Simulating"]
                    + [
                        f"{c_type.value.capitalize()}: {self.complexities[c_type][-1]:.2E}"
                        for c_type in relevant_types
                    ]
                )
                loadbar.update()
            self.next()

        if self.save:
            self.save_gifs(bitmaps_dir)

        return csv_path

    def create_csv_results_file(self) -> str:
        csvs_dir = self.results_dir / "csvs"
        os.makedirs(csvs_dir, exist_ok=True)
        parameters = self.parameters_to_str(self.parameters)
        filename = f"{parameters}.csv"
        results_path = csvs_dir / filename

        self.results_fields = ["Timestep"] + [
            c_type.value.capitalize() for c_type in self.complexities.keys()
        ]
        with open(results_path, "w") as results_file:
            writer = DictWriter(results_file, self.results_fields)
            writer.writeheader()
        return results_path

    def save_gifs(self, bitmaps_dir: Path):
        gifs_dir = self.results_dir / "gifs"
        os.makedirs(gifs_dir, exist_ok=True)
        for c_type in self.complexities.keys():
            gif_type = c_type.value
            parameters = self.parameters_to_str(self.parameters)
            gif_path = gifs_dir / f"{parameters}_{gif_type}.gif"
            generate_gif(bitmaps_dir / gif_type, gif_path)

    def create_bitmaps_results_folder(self) -> Path:
        bitmaps_dir = self.results_dir / "bitmaps"
        for param in self.parameters:
            bitmaps_dir /= param
        if os.path.exists(bitmaps_dir):
            shutil.rmtree(bitmaps_dir)
        return bitmaps_dir

    def save_results(self, results_path: Path):
        TIMESTEPS = self.results_fields[0]
        results = {TIMESTEPS: self.step}
        results.update(
            {
                c_type.value.capitalize(): c_vals[-1]
                for c_type, c_vals in self.complexities.items()
            }
        )
        with open(results_path, "a") as results_file:
            results_writer = DictWriter(results_file, self.results_fields)
            results_writer.writerow(results)

    def compute_complexities(self, c_type_to_arr: Dict[ArrayTypes, np.ndarray]):
        for c_type, arr in c_type_to_arr.items():
            c_val = zip_array(arr)
            self.complexities[c_type].append(c_val)

        # mdl_complexity, mdl_entropy = encoded_sizes(self.cells)
        # self.complexities[Complexities.MDL_COMPLEXITY].append(mdl_complexity)
        # self.complexities[Complexities.MDL_ENTROPY].append(mdl_entropy)

    def save_images(
        self,
        bitmaps_dir: Path,
        step: int,
        c_type_to_arr: Dict[ArrayTypes, np.ndarray],
    ):
        for c_type, arr in c_type_to_arr.items():
            if arr is None:
                continue
            type_dir = bitmaps_dir / c_type.value
            os.makedirs(type_dir, exist_ok=True)
            save_image(arr, type_dir / f"{step}.bmp", self.n)


def save_image(array, filename, n):
    data = np.ravel(array)
    image = Image.new("L", (n, n))
    image.putdata(data, 255, 0)
    image.save(filename)
