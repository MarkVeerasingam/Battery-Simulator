from pydantic import BaseModel, StrictStr, StrictFloat, Field
from typing import Optional, Dict

class SolverConfiguration(BaseModel):
    solver: StrictStr = Field(
        ..., 
        description="The solver used for simulation, can be 'CasadiSolver' or 'IDAKLUSolver'",
        example="CasadiSolver"
    )
    tolerance: Dict[str, StrictFloat] = Field(
        default={"atol": 1e-6, "rtol": 1e-6},
        description="The relative and absolute tolerance for the solver, default is 1e-6."
    )
    # only used in the CasadiSolver
    mode: Optional[StrictStr] = Field(
        default="safe",
        description="The solver speed of CasadiSolver, can be fast or safe. Default is safe.",
        example="safe"
    )
