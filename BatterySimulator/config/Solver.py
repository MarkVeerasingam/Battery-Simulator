from pydantic import BaseModel, StrictStr, StrictFloat, Field
from typing import Optional, Dict, List

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
    """Specifying output_variables is strongly recommended to reduce computational load, while inputs are only required when derivatives are to be considered. - https://docs.pybamm.org/en/latest/source/examples/notebooks/solvers/idaklu-jax-interface.html#:~:text=Specifying%20output_variables%20is%20strongly%20recommended%20to%20reduce%20computational%20load%2C%20while%20inputs%20are%20only%20required%20when%20derivatives%20are%20to%20be%20considered."""
    # i am handling it like this. If the user of the API wants to view specific output variables e.g. Current [A], they will solve for it first than gain access to the result
    output_variables: Optional[List[StrictStr]] = Field(
        default_factory=list,
        description="List of output variables to track during simulation. Default is an empty list.",
        example=["Voltage [V]", "Current [A]", "Discharge capacity [A.h]"]
    )
