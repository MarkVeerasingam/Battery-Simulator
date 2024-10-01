import pybamm
from config.Config import SolverConfiguration

class IDAKLUSolver:
    @staticmethod
    def create_idaklu_solver(config: SolverConfiguration):
        """Create IDAKLUSolver."""
        atol = config.tolerance.get("atol", 1e-6)  
        rtol = config.tolerance.get("rtol", 1e-6) 

        solver = pybamm.IDAKLUSolver(atol=atol, rtol=rtol)
        solver._on_extrapolation = "warn"
        return solver
