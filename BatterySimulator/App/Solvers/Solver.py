import pybamm
from config.Config import SolverConfiguration

class Solver:
    @staticmethod
    def create(config: SolverConfiguration):
        solver_type = config.solver
        atol = config.tolerance.get("atol", 1e-6)  
        rtol = config.tolerance.get("rtol", 1e-6) 
        mode = config.mode

        if solver_type == "CasadiSolver":
            if mode not in ["safe", "fast", "fast with events"]:
                raise ValueError(f"Invalid CasadiSolver mode: {mode}. Must be 'safe', 'fast', or 'fast with events'")
            solver = pybamm.CasadiSolver(mode=mode, atol=atol, rtol=rtol)
        elif solver_type == "IDAKLUSolver":
            solver = pybamm.IDAKLUSolver(atol=atol, rtol=rtol)
        else:
            raise ValueError("Invalid solver, must be 'CasadiSolver' or 'IDAKLUSolver'")

        solver._on_extrapolation = "warn"
        return solver
