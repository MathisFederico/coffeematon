import numpy as np
from phi.flow import (
    advect,
    fluid,
    Solve,
    CenteredGrid,
    extrapolation,
    StaggeredGrid,
    Box,
    tensor,
    channel,
    Sphere,
)

from coffeematon.automatons.automaton import Automaton, InitialStates


class FluidAutomaton(Automaton):
    NAME = "Fluid"

    def next(self):
        """Physics simulation."""
        self.smoke = advect.mac_cormack(self.smoke, self.velocity, dt=1)
        buoyancy_force = self.smoke * (0, -1) @ self.velocity
        self.velocity = (
            advect.semi_lagrangian(self.velocity, self.velocity, dt=1) + buoyancy_force
        )
        self.velocity, _ = fluid.make_incompressible(
            self.velocity, solve=Solve(max_iterations=5000)
        )
        self._smoke_to_cells()

    def _smoke_to_cells(self):
        self.cells = np.array(self.smoke.data).transpose()[::-1]

    def set_initial_state(self):
        self.smoke = CenteredGrid(
            0,
            extrapolation.BOUNDARY,
            x=self.n,
            y=self.n,
            bounds=Box(x=self.n, y=self.n),
        )  # sampled at cell centers
        self.velocity = StaggeredGrid(
            0, extrapolation.ZERO, x=self.n, y=self.n, bounds=Box(x=self.n, y=self.n)
        )  # sampled in staggered form at face centers

        if self.initial_state is InitialStates.CIRCULAR:
            INFLOW_LOCATION = tensor(
                (self.n // 2, self.n - self.n // 4), channel(vector="x,y")
            )
            INFLOW = 1 * CenteredGrid(
                Sphere(center=INFLOW_LOCATION, radius=self.n // 4),
                extrapolation.BOUNDARY,
                x=self.n,
                y=self.n,
                bounds=Box(x=self.n, y=self.n),
            )
        elif self.initial_state is InitialStates.UPDOWN:
            INFLOW = 1 * CenteredGrid(
                Box(x=self.n, y=(self.n // 2, self.n)),
                extrapolation.BOUNDARY,
                x=self.n,
                y=self.n,
                bounds=Box(x=self.n, y=self.n),
            )
        else:
            raise NotImplementedError()
        self.smoke += INFLOW
        self._smoke_to_cells()

    def timesteps(self):
        return max(5 * self.n, 100)
