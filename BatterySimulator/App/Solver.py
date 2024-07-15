import pybamm
from pydantic import BaseModel, StrictFloat, StrictStr, validator

CasadiSolver = "CasadiSolver"

class ConfigSolver(BaseModel):
    solver: StrictStr
    atol: StrictFloat = 1e-6
    rtol: StrictFloat = 1e-6

    @staticmethod
    def create_from_config(solver: str, atol: float = 1e-6, rtol: float = 1e-6):
        return ConfigSolver(solver=solver, atol=atol, rtol=rtol)
    
    @validator("solver")
    def validate_solver(cls, solver):
        if solver != CasadiSolver:
            raise ValueError("Invalid solver, must be CasadiSolver")
        return solver

    def set_solver(self):
        if self.solver == CasadiSolver:
            # purposley removed "mode" from the ConfigSolver objects. When i ran it in fast for any BPX model, it failed the solving process.
            solver = pybamm.CasadiSolver(mode="safe", atol=self.atol, rtol=self.rtol)
            solver._on_extrapolation = "warn"
            return solver
        else:
            raise ValueError ("Invalid Solver, must be set as CasadiSolver")
        
    def update_solver(self, solver=None, atol=None, rtol=None):
        if solver:
            self.solver = solver
        if atol:
            self.atol = atol
        if rtol:
            self.rtol = rtol