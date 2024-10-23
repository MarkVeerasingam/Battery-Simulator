from pydantic import BaseModel, StrictStr, Field
from typing import Optional

class ECMConfiguration(BaseModel):
    # DTO to setup Thevenin model https://docs.pybamm.org/en/latest/source/api/models/equivalent_circuit/thevenin.html
    # by default equivalent_circuit_model in pybamm is a Thevenin model
    equivalent_circuit_model: StrictStr = Field(
        default="Thevenin Equivalent Circuit Model",
        description="Consists of an OCV element, a resistor element, and a number of RC elements (by default 1). The model is coupled to two lumped thermal models, one for the cell and one for the surrounding jig",
        example="Thevenin Equivalent Circuit Model"
    )
    is_2RC: Optional[bool] = Field(
    default=False,
    description="If the Thevenin Model is a 2RC Model",
    example=False,
    )