import pybamm
from config.Solver import SolverConfiguration

class CasadiSolver:
    @staticmethod
    def create_casadi_solver(config: SolverConfiguration):
        """Create CasadiSolver."""
        mode = config.mode
        atol = config.tolerance.get("atol", 1e-6)  
        rtol = config.tolerance.get("rtol", 1e-6) 

        if mode not in ["safe", "fast", "fast with events"]:
            raise ValueError(f"Invalid CasadiSolver mode: {mode}. Must be 'safe', 'fast', or 'fast with events'")
        
        solver = pybamm.CasadiSolver(mode=mode, atol=atol, rtol=rtol)
        solver._on_extrapolation = "warn"
        return solver
