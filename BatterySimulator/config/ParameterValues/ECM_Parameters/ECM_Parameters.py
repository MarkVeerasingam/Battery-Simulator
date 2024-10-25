from pydantic import BaseModel, Field, StrictStr, StrictFloat
from typing import List, Optional

class TheveninParameters(BaseModel):
    R0: Optional[StrictFloat] = Field(
        default=1e-3,
        description="",
        example=1e-3
    )
    R1: Optional[StrictFloat] = Field(
        default=2e-4,
        description="",
        example=2e-4
    )
    R2: Optional[StrictFloat] = Field(
        default=0.0003,
        description="",
        example=0.0003
    )
    C1: Optional[StrictFloat] = Field(
        default=1e4,
        description="",
        example=1e4
    )
    C2: Optional[StrictFloat] = Field(
        default=40000,
        description="",
        example=40000
    )
    initial_state_of_charge: Optional[StrictFloat] = Field(
        default=0.5,
        description="Initial state of charge as a fraction between 0 and 1",
        example=0.5
    )
    upper_voltage_cut_off: Optional[StrictFloat] = Field(
        default=4.2,
        description="Upper voltage cut-off of the lithium-ion battery in volts",
        example=4.2
    )
    lower_voltage_cut_off: Optional[StrictFloat] = Field(
        default=3.0,
        description="Lower voltage cut-off of the lithium-ion battery in volts",
        example=3.0
    )
    cell_capacity: Optional[StrictFloat] = Field(
        default=5.0,
        description="Cell capacity of the lithium-ion battery in ampere-hours",
        example=5.0
    )
    nominal_cell_capacity: Optional[StrictFloat] = Field(
        default=5.0,
        description="Nominal cell capacity of the lithium-ion battery in ampere-hours",
        example=5.0
    )