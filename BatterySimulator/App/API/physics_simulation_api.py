from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from App.Simulations.SimulationRunner import SimulationRunner
from App.API.DTO.SimulationRequest import Physics_SimulationRequest
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

pybamm.set_logging_level("INFO")

@physics_app.post("/")
async def simulate(request: Physics_SimulationRequest):
    try:
        battery_config = request.parameter_values
        electrochemical_config = request.electrochemical_model
        solver_config = request.solver_model
        simulation_config = request.simulation

        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)
        sim_runner.run_simulation(config=simulation_config)

        display_params = request.display_params or ["Terminal voltage [V]"]
        results = sim_runner.display_results(display_params)

        return results

    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
