from pydantic import BaseModel, Field
from typing import List, Optional

class CircuitComponent(BaseModel):
    name: str = Field(
        ..., 
        description="The name of the circuit component, e.g., R0, R1, C1, C2 etc.",
        example="R0"
    )
    value: float = Field(
        ..., 
        description="The value of the circuit component (e.g., resistance in ohms or capacitance in farads).",
        example=1e-3
    )
    unit: str = Field(
        ..., 
        description="The unit of the circuit component, e.g., 'Ohm' for resistors, 'Farad' for capacitors.",
        example="Ohm"
    )

class CircuitConfiguration(BaseModel):
    is_2RC: bool = Field(
        default=False,
        description="If the Thevenin Model is a 2RC Model",
        example=False,
    )
    components: List[CircuitComponent] = Field(
        ..., 
        description="A list of circuit components for the model, each with a name, value, and unit."
    )
    initial_state_of_charge: Optional[float] = Field(
        default=0.5,
        description="Initial state of charge as a fraction between 0 and 1",
        example=0.5
    )
    upper_voltage_cut_off: Optional[float] = Field(
        default=4.2,
        description="Upper voltage cut-off of the lithium-ion battery in volts",
        example=4.2
    )
    lower_voltage_cut_off: Optional[float] = Field(
        default=3.0,
        description="Lower voltage cut-off of the lithium-ion battery in volts",
        example=3.0
    )
    cell_capacity: Optional[float] = Field(
        default=5.0,
        description="Cell capacity of the lithium-ion battery in ampere-hours",
        example=5.0
    )
    nominal_cell_capacity: Optional[float] = Field(
        default=5.0,
        description="Nominal cell capacity of the lithium-ion battery in ampere-hours",
        example=5.0
    )