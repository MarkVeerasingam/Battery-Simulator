from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from config.ParameterValues import ParameterValueConfiguration
from config.Models.PhysicsBasedModel import ElectrochemicalModelConfiguration
from config.Simulation import SimulationConfiguration, DriveCycleFile
from config.Solver import SolverConfiguration
from App.Simulations.SimulationRunner import SimulationRunner
import pybamm

# Initialize FastAPI
physics_app = FastAPI()

# Enable CORS
physics_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    parameter_values: ParameterValueConfiguration
    electrochemical_model: ElectrochemicalModelConfiguration
    solver_model: SolverConfiguration
    simulation: SimulationConfiguration
    display_params: Optional[List[str]] = None

# Logging configuration
pybamm.set_logging_level("INFO")

@physics_app.post("/")
async def simulate(request: SimulationRequest):
    try:
        # Extract the simulation + model configurations from the request
        battery_config = request.parameter_values
        electrochemical_config = request.electrochemical_model
        solver_config = request.solver_model
        simulation_config = request.simulation

        # Initialize the simulation runner
        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)
        # Run the simulation with the provided configuration
        sim_runner.run_simulation(config=simulation_config)

        # Get display parameters, defaulting if not provided
        display_params = request.display_params or ["Terminal voltage [V]"]
        results = sim_runner.display_results(display_params)

        return results

    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
