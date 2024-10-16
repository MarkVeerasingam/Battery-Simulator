from pydantic import BaseModel, StrictStr, Field
from typing import Optional, Dict

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
    updated_parameters: Optional[Dict[str, float]] = Field(
        default=None,
        description="Optional dictionary of parameter names and their new values, e.g., {'Current [A]': 5.0, 'Temperature [K]': 298.15}.",
        example={"Current [A]": 10.0, "Temperature [C]": 298.15}
    )

class ECM_ParameterValueConfiguration(BaseModel):
    R0: Dict[str, float] = Field(
        default={"R0 [Ohm]": 1e-3},
        description="R0 resistance in ohms",
        example={"R0 [Ohm]": 1e-3}
    )
    R1: Dict[str, float] = Field(
        default={"R1 [Ohm]": 2e-4},
        description="R1 resistance in ohms",
        example={"R1 [Ohm]": 2e-4}
    )
    R2: Dict[str, float] = Field(
        default={"R2 [Ohm]": 0.0003},
        description="R2 resistance in ohms",
        example={"R2 [Ohm]": 0.0003}
    )
    C1: Dict[str, float] = Field(
        default={"C1 [Farad]": 2e-4},
        description="C1 capacitance in farads",
        example={"C1 [Farad]": 2e-4}
    )
    C2: Dict[str, float] = Field(
        default={"C2 [Farad]": 0.0003},
        description="C2 capacitance in farads",
        example={"C2 [Farad]": 0.0003}
    )
    element_1_initial_overpotential: Dict[str, float] = Field(
        default={"Element-1 initial overpotential [V]": 0},
        description="Initial overpotential for element 1 in volts",
        example={"Element-1 initial overpotential [V]": 0}
    )
    element_2_initial_overpotential: Optional[Dict[str, float]] = Field(
        default=None,
        description="Initial overpotential for element 2 in volts, needed for 2 RC models",
        example={"Element-2 initial overpotential [V]": 0}
    )
    initial_state_of_charge: Dict[str, float] = Field(
        default={"Initial SoC": 0.5},
        description="Initial state of charge as a fraction between 0 and 1",
        example={"Initial SoC": 0.5}
    )
    upper_voltage_cut_off: Dict[str, float] = Field(
        default={"Upper voltage cut-off [V]": 4.2},
        description="Upper voltage cut-off of the lithium-ion battery in volts",
        example={"Upper voltage cut-off [V]": 4.2}
    )
    lower_voltage_cut_off: Dict[str, float] = Field(
        default={"Lower voltage cut-off [V]": 3.0},
        description="Lower voltage cut-off of the lithium-ion battery in volts",
        example={"Lower voltage cut-off [V]": 3.0}
    )
    cell_capacity: Dict[str, float] = Field(
        default={"Cell capacity [A.h]": 5},
        description="Cell capacity of the lithium-ion battery in ampere-hours",
        example={"Cell capacity [A.h]": 5}
    )
    nominal_cell_capacity: Dict[str, float] = Field(
        default={"Nominal cell capacity [A.h]": 5},
        description="Nominal cell capacity of the lithium-ion battery in ampere-hours",
        example={"Nominal cell capacity [A.h]": 5}
    )
