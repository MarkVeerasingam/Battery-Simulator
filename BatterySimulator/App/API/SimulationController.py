from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from App.Simulations.SimulationRunner import SimulationRunner
from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest
import pybamm

simulation_app = FastAPI()

simulation_app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pybamm.set_logging_level("INFO")

@simulation_app.post("/physics")
async def physics_simulate(request: Physics_SimulationRequest):
    try:
        battery_config = request.parameter_values
        electrochemical_config = request.electrochemical_model
        solver_config = request.solver_model
        simulation_config = request.simulation

        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)
        await sim_runner.run_simulation(config=simulation_config)

        display_params = request.display_params or ["Terminal voltage [V]"]
        results = sim_runner.display_results(display_params)

        return results

    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@simulation_app.post("/ecm")
async def ecm_simulate(request: ECM_SimulationRequest):
    try:
        parameter_value_config = request.parameter_values
        equivalent_circuit_model_config = request.equivalent_circuit_model
        solver_config = request.solver
        simulation_config = request.simulation

        sim_runner = ECM_SimulationRunner(parameter_value_config=parameter_value_config,
                                      solver_config=solver_config,
                                      ecm_config=equivalent_circuit_model_config)

        await sim_runner.run_simulation(simulation_config)

        display_params = request.display_params or ["Voltage [V]", "Current [A]", "Jig temperature [K]"]
        results = sim_runner.display_results(display_params)

        return results

    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
