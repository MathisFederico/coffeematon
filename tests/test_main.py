from coffeematon.automatons.fluid_automaton import FluidAutomaton
from coffeematon.automatons.int_automaton import InteractingAutomaton
from coffeematon.automatons.nonint_automaton import NonInteractingAutomaton


def test_int():
    automaton = InteractingAutomaton(10, save=False)
    automaton.simulate()


def test_nonint():
    automaton = NonInteractingAutomaton(10, save=False)
    automaton.simulate()


def test_fluid():
    automaton = FluidAutomaton(10, save=False)
    automaton.simulate()


def test_int_circular():
    automaton = InteractingAutomaton(10, initial_state="circular", save=False)
    automaton.simulate()


def test_nonint_circular():
    automaton = NonInteractingAutomaton(10, initial_state="circular", save=False)
    automaton.simulate()


def test_fluid_circular():
    automaton = FluidAutomaton(10, initial_state="circular", save=False)
    automaton.simulate()
