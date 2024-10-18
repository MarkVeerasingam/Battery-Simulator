import pybamm
from config.Solver import SolverConfiguration

class IDAKLUSolver:
    @staticmethod
    def create_idaklu_solver(config: SolverConfiguration):
        """Create IDAKLUSolver."""
        atol = config.tolerance.get("atol", 1e-6)  
        rtol = config.tolerance.get("rtol", 1e-6) 
        # output_variables unused as it throws errors for BPX LFP parameters but fine for others.
        # this addressed this issue with a closed pr: pybamm-team/PyBaMM#4440 after i flagged the issue: https://github.com/pybamm-team/PyBaMM/issues/4414 
        # need to wait for next release of pybamm
        # output_variables = config.output_variables
        
        solver = pybamm.IDAKLUSolver(atol=atol, rtol=rtol)
        solver._on_extrapolation = "warn"
        return solver