from pydantic import BaseModel, StrictStr, Field

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
