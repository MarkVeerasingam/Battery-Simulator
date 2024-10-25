from pydantic import BaseModel, Field, StrictFloat
from typing import Optional

class Update_Electrochemical_Parameters(BaseModel):
    current_function: Optional[StrictFloat] = Field(
        alias="Current function [A]",
        description="Current function [A]",
        default=10,
        example=10,
    )
    ambient_temperature: Optional[StrictFloat] = Field(
        alias="Ambient temperature [K]",
        description="Ambient temperature [K]",
        default=298.15,
        example=298.15,
    )