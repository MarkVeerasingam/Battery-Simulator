import pybamm
from config.Config import SolverConfiguration

class Solver:
    @staticmethod
    def create(config: SolverConfiguration):
        solver_type = config.solver

        # Default to 1e-6 if not provided
        atol = config.tolerance.get("atol", 1e-6)  
        rtol = config.tolerance.get("rtol", 1e-6) 

        # get the config mode for the casadi solver, default mode is "safe"
        mode = config.mode

        # crude check if the solver is CasadiSolver
        if solver_type != "CasadiSolver":
            raise ValueError("Invalid solver, must be CasadiSolver")
        
        # create solver in pybamm. need to make solver it's own class in Config.py to handle more parameterization
        solver = pybamm.CasadiSolver(mode=mode, atol=atol, rtol=rtol)
        solver._on_extrapolation = "warn"
        return solver