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