# The Coffee Automaton - Quantifying the Rise and Fall of Complexity in Closed Systems

[![Licence - GPLv3](https://img.shields.io/github/license/MathisFederico/CoffeeMaton?style=plastic)](https://www.gnu.org/licenses/)

[![CodeStyle - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CodeStyle - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

A reproduction of the paper [The Coffee Automaton - Quantifying the Rise and Fall of Complexity in Closed Systems](https://arxiv.org/abs/1405.6903).

This codebase started from the given code in the paper and was updated to python 3 with few changes to improve experiment speed. Moreover some additional feature were added such as a fluid-like automaton, different smoothing functions, and different initial states.

## A drop of milk in coffee

| ![Large fine circular drop gif](figures/bitmaps/circular/fluid/fine_bitmaps.gif) | ![Large coarse circular drop gif](figures/bitmaps/circular/fluid/coarse_bitmaps.gif) | ![Large adjusted coarse circular drop gif](figures/bitmaps/circular/fluid/adj_coarse_bitmaps.gif) |
| :--: | :--: | :--: |
| *Fine* | *Coarse* | *Adjusted coarse* |

## Entropy, Complexity and Sophistication

| ![Large fine updown drop gif](figures/bitmaps/updown/fluid/fine_bitmaps.gif) | ![Large coarse updown drop gif](figures/bitmaps/updown/fluid/coarse_bitmaps.gif) | ![Large adjusted coarse updown drop gif](figures/bitmaps/updown/fluid/adj_coarse_bitmaps.gif) |
| :--: | :--: | :--: |
| *Fine* | *Coarse* | *Adjusted coarse* |

## Reproduced results

Paper figure:
![Paper figure](figures/reproduced/paper_figures/The-estimated-entropy-and-complexity-of-an-automaton-using-the-coarse-graining-metric.png)

Reproduced figures:

Note that in our codebase and for the sake of accuracy and generalisation, we replaced "complexity" by the "coarse_3" size and "entropy" by the "fine" size.

| *Interacting* | *Non-Interacting* |
| :--: | :--: |
| ![Interacting gif](figures/reproduced/updown_interacting_100_fine.gif) | ![Non-Interacting gif](figures/reproduced/updown_non-interacting_100_fine.gif) |
| ![Interacting results](figures/reproduced/updown_interacting_100_linscale.png) | ![Non-Interacting results](figures/reproduced/updown_non-interacting_100_linscale.png) |
| ![Alt text](figures/reproduced/updown_interacting_100.png) | ![Alt text](figures/reproduced/updown_non-interacting_100.png) |
| Interacting automaton takes more step because we count steps when two identical cells are choosen to be swaped, but results are fairly similar for both complexity and entropy. | Non-interacting automaton results couldn't be reproduced, even in loglog scale we cannot see any sign of complexity increase during the experiment even if the entropy is identical. |





## Added Features

### Circular initial state

Instead of starting with a half coffee / half milk initial state we called **updown**. You can now initialize a circle of milk in the center and coffee all around, called the **circular** initial state.


| *Updown* | *Circular* |
|:--:| :--: |
| ![Updown initial state](figures/init_states_examples/init_updown.bmp) | ![Circular initial state](figures/init_states_examples/init_circular.bmp) |
| ![Updown initial state gif](figures/reproduced/updown_interacting_100_fine.gif) | ![Circular initial state gif](figures/init_states_examples/circular_interacting_100_fine.gif) |


### Other smoothing functions
 - Generalisation of the coarse-graining function to $k\in N^*, k>2$ categories. In the paper, they take 3 for the initial coarse-graining and 7 for the adujsted coarse-graining.
 - **Diff**erences [0.5 if f(x) == x else x] for each coarse-graining.
 - Differences **Mask** [f(x) == x] for each coarse-graining.


| *Fine* | *Coarse_3* | *Coarse_7* | *Coarse_11* | *Diff_3* | *Diff_7* | *Diff_11* | *Mask_3* | *Mask_7* | *Mask_11* |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| ![Fine gif](figures/reproduced/updown_interacting_100_fine.gif) | ![Coarse_3 gif](figures/other_smoothing_functions_examples/updown_interacting_100_coarse_3.gif) | ![Coarse_7 gif](figures/other_smoothing_functions_examples/updown_interacting_100_coarse_7.gif) | ![Coarse_11 gif](figures/other_smoothing_functions_examples/updown_interacting_100_coarse_11.gif) | ![Diff_3 gif](figures/other_smoothing_functions_examples/updown_interacting_100_diff_3.gif) | ![Diff_7 gif](figures/other_smoothing_functions_examples/updown_interacting_100_diff_7.gif) | ![Diff_11 gif](figures/other_smoothing_functions_examples/updown_interacting_100_diff_11.gif) | ![Mask_3 gif](figures/other_smoothing_functions_examples/updown_interacting_100_mask_3.gif) | ![Mask_7 gif](figures/other_smoothing_functions_examples/updown_interacting_100_mask_7.gif) | ![Mask_11 gif](figures/other_smoothing_functions_examples/updown_interacting_100_mask_11.gif) |

### Fluid automaton

| *Interacting* | *Non-Interacting* | *Fluid* |
| :--: | :--: | :--: |
| ![Interacting gif](figures/reproduced/updown_interacting_100_fine.gif) | ![Non-Interacting gif](figures/reproduced/updown_non-interacting_100_fine.gif) | ![Fluid gif](figures/updown_fluid_100_fine.gif) |


## Installation

### Using pip

```bash
pip install git+https://github.com/MathisFederico/coffeematon.git
```

### From source

```bash
git clone https://github.com/MathisFederico/coffeematon.git
```

Then inside the worspace:
```bash
pip install -e .
```

## Quickstart

Launch an experiment
```bash
python -m coffeematon --help
```

Plot a graph from a csv results file
```bash
python -m coffeematon.plot_results --help
```

Generate a gif from bitmaps
```bash
python -m coffeematon.generate_gifs --help
```


## Results

| Initial state | Automaton type | Size | Graph |
|---------------|----------------|------|-------|
| Updown | Interacting | 100 | ![updown_interacting_100](figures/graphs/updown_interacting_100.png) |
| Updown | Interacting | 200 | ![updown_interacting_200](figures/graphs/updown_interacting_200.png) |
| Circular | Interacting | 100 | ![circular_interacting_100](figures/graphs/circular_interacting_100.png) |
| Circular | Interacting | 200 | ![circular_interacting_200](figures/graphs/circular_interacting_200.png) |
| Updown | Fluid | 100 | ![updown_fluid_100](figures/graphs/updown_fluid_100.png) |
| Updown | Fluid | 200 | ![updown_fluid_200](figures/graphs/updown_fluid_200.png) |
| Circular | Fluid | 100 | ![circular_fluid_100](figures/graphs/circular_fluid_100.png) |
| Circular | Fluid | 200 | ![circular_fluid_200](figures/graphs/circular_fluid_200.png) |
| Updown | Non-Interacting | 100 | ![updown_non-interacting_100](figures/graphs/updown_non-interacting_100.png) |
| Updown | Non-Interacting | 200 | ![updown_non-interacting_100](figures/graphs/updown_non-interacting_200.png) |
| Circular | Non-Interacting | 100 | ![circular_non-interacting_100](figures/graphs/circular_non-interacting_100.png) |
| Circular | Non-Interacting | 200 | ![circular_non-interacting_200](figures/graphs/circular_non-interacting_200.png) |

