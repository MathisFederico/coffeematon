"""
Collecting automaton output
"""

from time import time
import argparse
from typing import Dict, Optional
import matplotlib.pyplot as plt
import numpy

from coffeematon.automatons.automaton import Automaton, Complexities, InitialStates
from coffeematon.automatons.nonint_automaton import NonInteractingAutomaton
from coffeematon.automatons.int_automaton import InteractingAutomaton
from coffeematon.automatons.fluid_automaton import FluidAutomaton
from coffeematon.generate_gifs import generate_gif

AUTOMATONS: Dict[str, Automaton] = {
    "nonint": NonInteractingAutomaton,
    "int": InteractingAutomaton,
    "fluid": FluidAutomaton,
}


def experiment_for_n(automaton_type: str, n: int, init: Optional[InitialStates] = None):
    automaton: Automaton = AUTOMATONS.get(automaton_type)(n, init)

    t_start = time()
    automaton.simulate()
    t_end = time()

    # Print and save statistics
    with open(automaton.dir / f"stats_{n}", "w") as stats_file:
        stats_file.write(f"steps = {automaton.steps}\n")
        for c_type, c_vals in automaton.complexities.items():
            stats_file.write(f"{c_type.value.capitalize()} = {c_vals}\n")

    # Generate and save plots
    plt.figure()
    plt.title(f"{automaton.NAME} Automaton, n={automaton.n}")
    plt.xlabel("Time step")
    plt.ylabel("Encoded size, bytes")

    for c_type, c_vals in automaton.complexities.items():
        plt.plot(automaton.steps, c_vals, label=c_type.value.capitalize())

    plt.legend()
    plt.savefig(automaton.dir / "graph")
    plt.close()

    print("Time for n=%d: %d sec." % (automaton.n, t_end - t_start))

    for gif_type in ["fine", "coarse", "adj_coarse", "diff"]:
        generate_gif(automaton.dir / "bitmaps" / gif_type)

    # Return statistics
    mix_time = automaton.step
    emax_val = max(automaton.complexities[Complexities.ENTROPY])
    cmax_time = automaton.steps[
        numpy.argmax(automaton.complexities[Complexities.ADJ_COARSE])
    ]
    cmax_val = max(automaton.complexities[Complexities.ADJ_COARSE])
    return (mix_time, emax_val, cmax_time, cmax_val)


def data_for_range(type, start, stop, step=1):
    ns = range(start, stop, step)
    mix_times = []
    emax_vals = []
    cmax_times = []
    cmax_vals = []

    t1 = time()
    for n in ns:
        # Collect statistics for each value of n
        (mix_time, emax_val, cmax_time, cmax_val) = experiment_for_n(type, n)
        mix_times.append(mix_time)
        emax_vals.append(emax_val)
        cmax_times.append(cmax_time)
        cmax_vals.append(cmax_val)
    t2 = time()
    print(f"Total time: {t2 - t1:d} sec.")

    # Save statistics to file
    f = open("stats_%s_%d_%d" % (type, start, stop - step), "w")
    f.write("ns = " + str(ns) + "\n")
    f.write("mix_times = " + str(mix_times) + "\n")
    f.write("emax_vals = " + str(emax_vals) + "\n")
    f.write("cmax_times = " + str(cmax_times) + "\n")
    f.write("cmax_vals = " + str(cmax_vals) + "\n")
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--automaton",
        choices=AUTOMATONS.keys(),
        help="Type of automaton to use.",
        required=True,
    )
    parser.add_argument(
        "-n",
        help="Size of the automaton.",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--init",
        help="Initial state of the automaton.",
        choices=[i.value for i in InitialStates],
        default="updown",
    )
    args = parser.parse_args()
    experiment_for_n(args.automaton, args.n, args.init)


if __name__ == "__main__":
    main()
