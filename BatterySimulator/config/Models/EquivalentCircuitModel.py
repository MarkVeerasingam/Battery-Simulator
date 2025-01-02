from pydantic import BaseModel, StrictStr, Field, conint, StrictInt
from typing import Optional

class ECMConfiguration(BaseModel):
    # DTO to setup Thevenin model https://docs.pybamm.org/en/latest/source/api/models/equivalent_circuit/thevenin.html
    # by default equivalent_circuit_model in pybamm is a Thevenin model
    # equivalent_circuit_model: StrictStr = Field(
    #     default="Thevenin Equivalent Circuit Model",
    #     description="Consists of an OCV element, a resistor element, and a number of RC elements (by default 1). The model is coupled to two lumped thermal models, one for the cell and one for the surrounding jig",
    #     example="Thevenin Equivalent Circuit Model"
    # )
    RC_pairs: Optional[StrictInt] = Field(
        default=1,
        description="Specifies the number of RC elements in the Thevenin Model. Max value is 2RC. Default is 1RC. If left blank default is 1RC pair",
        example=2,
    )