from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from config.Models.PhysicsBasedModel import ElectrochemicalModelConfiguration
from config.Simulation import SimulationConfiguration
from config.Solver import SolverConfiguration
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4

class ECM_SimulationRequest(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))    
    equivalent_circuit_model: ECMConfiguration
    parameter_values: ParameterValueConfiguration
    solver: SolverConfiguration
    simulation: SimulationConfiguration
    display_params: Optional[List[str]]

class Physics_SimulationRequest(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))    
    parameter_values: ParameterValueConfiguration 
    electrochemical_model: ElectrochemicalModelConfiguration 
    solver_model: SolverConfiguration
    simulation: SimulationConfiguration 
    display_params: Optional[List[str]] 