import os
import argparse
import matplotlib.pyplot as plt
from pathlib import Path
from csv import DictReader

from typing import Optional, Dict, List

from coffeematon.automatons.automaton import Automaton


def plot_results(
    csv_results_path: Path,
    graph_path: Optional[Path] = None,
    choosen_complexites: Optional[List[str]] = None,
    linscale: bool = False,
):
    csv_results_path = Path(csv_results_path)
    if graph_path is None:
        graph_path = (
            csv_results_path.parent.parent
            / "graphs"
            / csv_results_path.name.replace(".csv", ".png")
        )
    graph_path = Path(graph_path)
    os.makedirs(graph_path.parent, exist_ok=True)

    results_data: Dict[str, list] = {}

    with open(csv_results_path, "r") as csv_results_file:
        results = DictReader(csv_results_file)
        FIELDS = results.fieldnames
        for field in FIELDS:
            results_data[field] = []
        for results_dict in results:
            for field, value in results_dict.items():
                results_data[field].append(int(value))

    steps = results_data.pop(FIELDS[0])
    complexities = results_data
    if choosen_complexites is not None:
        complexities = {
            k: v for k, v in complexities.items() if k.lower() in choosen_complexites
        }

    initstate, name, n = Automaton.str_to_parameters(
        csv_results_path.name.removesuffix(".csv")
    )

    plt.figure()
    plt.title(f"{name.capitalize()} Automaton with initial state {initstate} (n={n})")
    plt.xlabel("Time step")
    plt.ylabel("Encoded size (bytes)")

    for c_type, c_vals in complexities.items():
        plt.plot(steps, c_vals, label=c_type)

    plt.legend()
    if not linscale:
        plt.loglog()
    plt.savefig(graph_path)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Path to the csv results file.")
    parser.add_argument(
        "-o", "--save", help="Path where to save the plot.", default=None
    )
    parser.add_argument(
        "-c",
        "--complexities",
        help="Complexities to plot.",
        default=None,
        nargs="*",
    )
    parser.add_argument(
        "--linscale",
        help="Set to linear scale instead of default loglog scale.",
        action="store_true",
    )
    args = parser.parse_args()
    plot_results(args.csv_path, args.save, args.complexities, args.linscale)
