import pybamm
from flask import Blueprint, request, jsonify

simulateLFP_experiment_bp = Blueprint("LFP_experimentSimulation", __name__)

def load_parameters(filepath):
    """Load parameters from a BPX JSON file."""
    return pybamm.ParameterValues.create_from_bpx(filepath)

def create_model():
    # Create a DFN model
    model = pybamm.lithium_ion.DFN()
    return model

def create_solver():
    # solver
    solver = pybamm.CasadiSolver("safe", atol=1e-6, rtol=1e-6)
    # Prevent solver failure if interpolant bounds are exceeded by a negligible amount
    solver._on_extrapolation = "warn"
    return solver

# for now i want to integrate this to a front end to reorder the existing 
def define_experiment(experiment_lines):
    # Example experiment
    # experiment = pybamm.Experiment(
    #     [
    #         (
    #             "Discharge at C/5 for 10 hours or until 2.5 V",
    #             "Rest for 1 hour",
    #             "Charge at 1 A until 3.5 V",
    #             "Hold at 3.5 V until 10 mA",
    #             "Rest for 1 hour",
    #         ),
    #     ]
    #     * 2
    # )
    experiment = pybamm.Experiment(experiment_lines)
    return experiment

def run_simulation(parameter_file, experiment_lines):
    try:
        # Import parameters from BPX JSON file
        parameter_values = load_parameters(parameter_file)

        model = create_model()

        solver = create_solver()

        experiment = define_experiment(experiment_lines)

        # Create a simulation object
        sim = pybamm.Simulation(model, parameter_values=parameter_values, solver=solver, experiment=experiment)

        # Simulate
        solution = sim.solve()

        # Plot results
        # sim.plot(
        # [
        #     ["Electrode current density [A.m-2]", "Electrolyte current density [A.m-2]"],
        #     "Voltage [V]",
        #     "Current [A]"
        # ]
        # )

        # Extract simulation results
        # contents of the payload sent to job manager.
        time_s = solution['Time [s]'].entries
        voltage = solution['Battery voltage [V]'].entries
        current = solution['Current [A]'].entries
        discharge_cap = solution['Discharge capacity [A.h]'].entries
        combined_data = []

        # Format results for JSON response
        for i in range(len(time_s)):
            data_point = {
                "time": time_s[i],
                "voltage": voltage[i],
                "current": current[i],
                "discharge_capacity": discharge_cap[i]
            }
            combined_data.append(data_point)

        return combined_data # return the formatted simulation results
    except Exception as e:
            raise RuntimeError(f"Simulation failed: {str(e)}")

@simulateLFP_experiment_bp.route('/simulate', methods=['POST'])
def simulate_battery_experiment():
    try:
        data = request.get_json()

        # Import parameters from BPX JSON file
        parameter_file = "BatterySimulator_SimulationBackend/LFP/lfp_18650_cell_BPX.json"

        """Custom Simulation"""
        # Extract experiment lines from POST request
        experiment_lines = data.get('experimentLines', [])
        if not experiment_lines:
            raise ValueError("Experiment lines not provided in the request")

        # Run simulation with custom experiment lines
        simulation_results = run_simulation(parameter_file, experiment_lines)

        """Default simulation"""
        return jsonify({
            "success": True,
            "results": simulation_results
            })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
if __name__ == "__main__":
    experiment_lines = [
        (
            "Discharge at C/5 for 10 hours or until 2.5 V",
            "Rest for 1 hour",
            "Charge at 1 A until 3.5 V",
            "Hold at 3.5 V until 10 mA",
            "Rest for 1 hour",
        ),
    ] * 2

    parameter_file = "BatterySimulator_SimulationBackend/LFP/lfp_18650_cell_BPX.json"
    run_simulation(parameter_file, experiment_lines)
