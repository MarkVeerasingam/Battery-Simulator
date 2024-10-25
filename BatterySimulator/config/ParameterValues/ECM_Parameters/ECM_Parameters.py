from pydantic import BaseModel, Field, StrictFloat, StrictInt
from typing import  Optional

class TheveninParameters(BaseModel):
    R0: Optional[StrictFloat] = Field(
        alias="R0 [Ohm]",
        description="",
        default=1e-3,
        example=1e-3
    )
    R1: Optional[StrictFloat] = Field(
        alias="R1 [Ohm]",
        description="",
        default=2e-4,
        example=2e-4
    )
    R2: Optional[StrictFloat] = Field(
        alias="R2 [Ohm]",
        description="",
        default=0.0003,
        example=0.0003
    )
    C1: Optional[StrictFloat] = Field(
        alias="C1 [F]",
        description="",
        default=1e4,
        example=1e4
    )
    C2: Optional[StrictFloat] = Field(
        alias="C2 [F]",
        description="",
        default=40000,
        example=40000
    )
    initial_state_of_charge: Optional[StrictFloat] = Field(
        alias="Initial SoC",
        description="Initial state of charge as a fraction between 0 and 1",
        default=0.5,
        example=0.5
    )
    upper_voltage_cut_off: Optional[StrictFloat] = Field(
        alias="Upper voltage cut-off [V]",
        description="Upper voltage cut-off of the lithium-ion battery in volts",
        default=4.2,
        example=4.2
    )
    lower_voltage_cut_off: Optional[StrictFloat] = Field(
        alias="Lower voltage cut-off [V]",
        description="Lower voltage cut-off of the lithium-ion battery in volts",
        default=3.0,
        example=3.0
    )
    cell_capacity: Optional[StrictFloat] = Field(
        alias="Cell capacity [A.h]",
        description="Cell capacity of the lithium-ion battery in ampere-hours",
        default=5.0,
        example=5.0
    )
    nominal_cell_capacity: Optional[StrictFloat] = Field(
        alias="Nominal cell capacity [A.h]",
        description="Nominal cell capacity of the lithium-ion battery in ampere-hours",
        default=5.0,
        example=5.0
    )
