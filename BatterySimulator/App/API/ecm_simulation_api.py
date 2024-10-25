from fastapi import APIRouter

ecm_app = APIRouter()

@ecm_app.get("/")
async def run_ecm_test():
    """
    Endpoint to run the ECM simulation test.
    """
    result = test_ecm_simulation()
    return {"status": "success", "data": result}


# test for ecm

from App.Simulations.ECMSimulationRunner import SimulationRunner
from App.ParameterValues.ParameterValuesRunner import ParameterValuesRunner
from App.Solvers.SolverRunner import SolverRunner
from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from config.Simulation import SimulationConfiguration
from config.Solver import SolverConfiguration


def test_ecm_simulation():
    parameter_value_config = ParameterValueConfiguration(
        parameter_value="ECM_Example", 
        is_bpx=False,
        updated_parameters={
            "Cell capacity [A.h]": 5,
            "Nominal cell capacity [A.h]": 5,
            "Current function [A]": 5,
            "Initial SoC": 0.5,
            "Element-1 initial overpotential [V]": 0,
            "Upper voltage cut-off [V]": 4.2,
            "Lower voltage cut-off [V]": 3.0,
            "R0 [Ohm]": 1e-3,
            "R1 [Ohm]": 2e-4,
            "C1 [F]": 1e4,
        }
    )

    ecm_config = ECMConfiguration(
        RC_pairs=1
    )

    solver_config = SolverConfiguration(
        solver="IDAKLUSolver",
        tolerance={"atol": 1e-6, "rtol": 1e-6},
        mode="safe"
    )

    simulation_config = SimulationConfiguration(
        experiment=(
            "Discharge at C/10 for 1 hour or until 3.3 V",
            "Rest for 30 minutes",
            "Rest for 2 hours",
            "Charge at 100 A until 4.1 V",
            "Hold at 4.1 V until 5 A",
            "Rest for 30 minutes",
            "Rest for 1 hour",
        )
    )

    runner = SimulationRunner(parameter_value_config, solver_config, ecm_config)
    
    # Run the simulation
    runner.run_simulation(simulation_config)

    # Display results for selected parameters
    selected_params = ["Voltage [V]", "Current [A]", "Jig temperature [K]"]
    results = runner.display_results(selected_params)
    return results
