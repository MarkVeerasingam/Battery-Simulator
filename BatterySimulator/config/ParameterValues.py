from pydantic import BaseModel, StrictStr, Field
from typing import Optional, Dict

class ParameterValueConfiguration(BaseModel):
    is_bpx: bool = Field(
        default=False,
        description="If the parameter value is a BPX model or not, used as logic to toggle between built-in pybamm parameter sets and bpx parameter sets.",
        example=True,
    )
    parameter_value: StrictStr = Field(
        ..., 
        description="The specific battery model name",
        example="lfp_18650_cell_BPX"
    )
    updated_parameters: Optional[Dict[str, float]] = Field(
        default=None,
        description="Optional dictionary of parameter names and their new values, e.g., {'Current [A]': 5.0, 'Temperature [K]': 298.15}.",
        example={"Current [A]": 10.0, "Temperature [C]": 298.15}
    )