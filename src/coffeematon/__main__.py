"""
Collecting automaton output
"""

from time import time
import matplotlib.pyplot as plt
import numpy

from coffeematon.automaton import Automaton, metrics
from coffeematon.nonint_automaton import NonInteractingAutomaton


def data_for_n(metric, type, n):
    t1 = time()
    if type == "nonint":
        a = NonInteractingAutomaton(n, metric)
    else:
        a = Automaton(n, metric)
    a.simulate()
    t2 = time()

    # Print and save statistics
    with open(a.dir / f"stats_{n}", "w") as stats_file:
        stats_file.write(f"x = {a.x}\n")
        stats_file.write(f"complexities = {a.complexities}\n")
        stats_file.write(f"entropies = {a.entropies}")

    # Generate and save plots
    typename = "Interacting"
    if type == "nonint":
        typename = "Non-Interacting"
    plt.figure()
    plt.title("%s Automaton, n=%d, %s" % (typename, a.n, metrics[a.metric]))
    plt.xlabel("Time step")
    plt.ylabel("Encoded size, bytes")
    plt.plot(a.x, a.complexities, "g-", label="Complexity")
    plt.plot(a.x, a.entropies, "b-", label="Entropy")
    plt.legend()
    plt.savefig(a.dir / "graph")
    plt.close()

    print("Time for n=%d: %d sec." % (a.n, t2 - t1))

    # Return statistics
    mix_time = a.step
    emax_val = max(a.entropies)
    cmax_time = a.x[numpy.argmax(a.complexities)]
    cmax_val = max(a.complexities)
    return (mix_time, emax_val, cmax_time, cmax_val)


def data_for_range(metric, type, start, stop, step=1):
    ns = range(start, stop, step)
    mix_times = []
    emax_vals = []
    cmax_times = []
    cmax_vals = []

    t1 = time()
    for n in ns:
        # Collect statistics for each value of n
        (mix_time, emax_val, cmax_time, cmax_val) = data_for_n(metric, type, n)
        mix_times.append(mix_time)
        emax_vals.append(emax_val)
        cmax_times.append(cmax_time)
        cmax_vals.append(cmax_val)
    t2 = time()
    print(f"Total time: {t2 - t1:d} sec.")

    # Save statistics to file
    f = open("stats_%s_%s_%d_%d" % (type, metric, start, stop - step), "w")
    f.write("ns = " + str(ns) + "\n")
    f.write("mix_times = " + str(mix_times) + "\n")
    f.write("emax_vals = " + str(emax_vals) + "\n")
    f.write("cmax_times = " + str(cmax_times) + "\n")
    f.write("cmax_vals = " + str(cmax_vals) + "\n")
    f.close()


def main():
    data_for_n("acg", "int", 100)
    data_for_n("acg", "nonint", 100)


if __name__ == "__main__":
    main()
