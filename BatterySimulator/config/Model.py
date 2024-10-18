from pydantic import BaseModel, StrictStr, Field
from typing import Optional

class ElectrochemicalModelConfiguration(BaseModel):
    electrochemical_model: StrictStr = Field(
        default="DFN",
        description="The name of the electrochemical model",
        example="DFN"
    )
    # set these as optional, however the default pybamm options of the electrochemical is cell_geometry: 'arbitrary', thermal: 'isothermal'
    # https://docs.pybamm.org/en/stable/source/examples/notebooks/models/using-model-options_thermal-example.html
    thermal_model: Optional[StrictStr] = Field(
        description="The thermal model option forq the battery simulation",
        example="isothermal"
    )
    cell_geometry: Optional[StrictStr] = Field(
        description="The cell geometry option for the battery simulation",
        example="arbitrary"
    )
    
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