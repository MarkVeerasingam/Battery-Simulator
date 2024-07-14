import pybamm
from pydantic import StrictStr, StrictFloat, validator, BaseModel

class SetupSolver(BaseModel):
    solver: StrictStr
    atol: StrictFloat = 1e-6
    rtol: StrictFloat = 1e-6

    @validator("solver")
    def validate_solver(cls, solver):
        if solver != "CasadiSolver":
            raise ValueError("Invalid solver, must be CasadiSolver")
        return solver
    
    def configure_and_get_solver(self):
        if self.solver == "CasadiSolver":
            return self.configure_casadi_solver()
        else:
            raise ValueError(f"Unknown solver type: {self.solver}")

    def configure_casadi_solver(self):
        solver = pybamm.CasadiSolver(mode="safe", atol=self.atol, rtol=self.rtol)
        solver._on_extrapolation = "warn"
        return solver