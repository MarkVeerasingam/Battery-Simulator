from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from config.Models.PhysicsBasedModel import ElectrochemicalModelConfiguration
from config.Simulation import SimulationConfiguration
from config.Solver import SolverConfiguration
from pydantic import BaseModel
from typing import Optional, List

class ECM_SimulationRequest(BaseModel):
    equivalent_circuit_model: ECMConfiguration
    parameter_values: ParameterValueConfiguration
    solver: SolverConfiguration
    simulation: SimulationConfiguration
    display_params: Optional[List[str]] = None

class Physics_SimulationRequest(BaseModel):
    parameter_values: ParameterValueConfiguration
    electrochemical_model: ElectrochemicalModelConfiguration
    solver_model: SolverConfiguration
    simulation: SimulationConfiguration
    display_params: Optional[List[str]] = None