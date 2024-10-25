from pydantic import BaseModel, Field, StrictFloat
from typing import Optional

class ElectrochemicalParameters(BaseModel):
    terminal_voltage: Optional[StrictFloat] = Field(
        default=1e-3,
        description="Terminal voltage [V]",
        example=1e-3,
        alias="Terminal voltage [V]"
    )
    current: Optional[StrictFloat] = Field(
        default=1e-3,
        description="Current [A]",
        example=1e-3,
        alias="Current [A]",
    )
    discharge_capacity: Optional[StrictFloat] = Field(
        default=1e-3,
        description="Discharge capacity [A.h]",
        example=1e-3,
        alias="Discharge capacity [A.h]"
    )
    ambient_temperature: Optional[StrictFloat] = Field(
        default=1e-3,
        description="Ambient temperature [K]",
        example=1e-3,
        alias="Ambient temperature [K]"
    )
    x_averaged_cell_temperature: Optional[StrictFloat] = Field(
        default=1e-3,
        description="X-averaged cell temperature [C]",
        example=1e-3,
        alias="X-averaged cell temperature [C]"
    )
    