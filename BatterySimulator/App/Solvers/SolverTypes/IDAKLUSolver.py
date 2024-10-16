import pybamm
from config.Solver import SolverConfiguration

class IDAKLUSolver:
    @staticmethod
    def create_idaklu_solver(config: SolverConfiguration):
        """Create IDAKLUSolver."""
        atol = config.tolerance.get("atol", 1e-6)  
        rtol = config.tolerance.get("rtol", 1e-6) 
        output_variables = config.output_variables
        
        solver = pybamm.IDAKLUSolver(atol=atol, rtol=rtol, output_variables=output_variables)
        solver._on_extrapolation = "warn"
        return solver
