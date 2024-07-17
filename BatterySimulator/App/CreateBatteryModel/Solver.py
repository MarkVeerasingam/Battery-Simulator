import pybamm

class Solver:
    @staticmethod
    def create(solver_type: str, atol: float, rtol: float):
        if solver_type != "CasadiSolver":
            raise ValueError("Invalid solver, must be CasadiSolver")
        
        solver = pybamm.CasadiSolver(mode="safe", atol=atol, rtol=rtol)
        solver._on_extrapolation = "warn"
        return solver