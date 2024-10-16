from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config.ParameterValues import ParameterValueConfiguration
from config.Model import ElectrochemicalModelConfiguration
from config.Simulation import SimulationConfiguration, DriveCycleFile
from config.Solver import SolverConfiguration
from App.Simulations.SimulationRunner import SimulationRunner
import pybamm

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models to validate incoming requests
class SimulationRequest(BaseModel):
    parameter_values: dict = None
    electrochemical_model: dict = None
    solver_model: dict = None
    simulation: dict = None
    display_params: list = None

# Logging configuration
pybamm.set_logging_level("INFO")

@app.post("/simulate")
async def simulate(request: SimulationRequest):
    try:
        # Extract data from request
        parameter_values = request.parameter_values or {}
        battery_config = ParameterValueConfiguration(
            is_bpx=parameter_values.get('is_bpx', True),
            parameter_value=parameter_values.get('parameter_values', 'NMC_Pouch_cell'),
            updated_parameters=parameter_values.get('updated_parameters', None)  # optional
        )

        electrochemical_data = request.electrochemical_model or {}
        electrochemical_config = ElectrochemicalModelConfiguration(
            electrochemical_model=electrochemical_data.get('model', 'DFN'),
            cell_geometry=electrochemical_data.get('cell_geometry', 'arbitrary'),
            thermal_model=electrochemical_data.get('thermal_model', 'isothermal')
        )

        solver_data = request.solver_model or {}
        solver_config = SolverConfiguration(
            solver=solver_data.get('solver', 'CasadiSolver'),
            tolerance=solver_data.get('tolerance', {"atol": 1e-6, "rtol": 1e-6}),
            mode=solver_data.get('mode', 'safe'),
            # output_variables=solver_data.get('output_variables', []) # removed until next pybamm version
        )

        simulation_data = request.simulation or {}
        simulation_type = simulation_data.get('type')

        if simulation_type == 'drive_cycle':
            drive_cycle = simulation_data.get('drive_cycle', {})
            simulation_config = SimulationConfiguration(
                drive_cycle=DriveCycleFile(
                    drive_cycle_file=drive_cycle.get('drive_cycle_file', 'NMC_25degC_1C')
                )
            )
        elif simulation_type == 'experiment':
            conditions = simulation_data.get('experiment', {}).get('conditions', [
                "Discharge at C/5 for 10 hours or until 2.5 V",
                "Rest for 1 hour",
                "Charge at 1 A until 3.5 V",
                "Hold at 3.5 V until 10 mA",
                "Rest for 1 hour"
            ])
            simulation_config = SimulationConfiguration(
                experiment=conditions
            )
        elif simulation_type == 'time_eval':
            conditions = simulation_data.get('time_eval', {}).get('conditions', [0, 7200])
            simulation_config = SimulationConfiguration(
                t_eval=conditions
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid simulation type")

        # Initialize the simulation runner
        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)

        # Run simulation
        sim_runner.run_simulation(config=simulation_config)

        # Get the display parameters from the request, default params are below, if not provided
        display_params = request.display_params or ["Terminal voltage [V]"]

        # Display the simulation results based on the requested parameters
        results = sim_runner.display_results(display_params)

        return results

    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
