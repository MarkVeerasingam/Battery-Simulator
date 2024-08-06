from flask import Flask, request, jsonify
from flask_cors import CORS
from config.Config import BatteryConfiguration, SolverConfiguration, DriveCycleFile, SimulationConfiguration
from App.SimulationRunner import SimulationRunner

app = Flask(__name__)
CORS(app)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json

    battery_config = BatteryConfiguration(
        battery_chemistry=data.get('battery_chemistry', 'NMC'),
        bpx_battery_models=data.get('bpx_battery_models', 'NMC_Pouch_cell'),
        electrochemical_model=data.get('electrochemical_model', 'DFN')
    )

    solver_config = SolverConfiguration(
        solver=data.get('solver', 'CasadiSolver'),
        tolerance=data.get('tolerance', {"atol": 1e-6, "rtol": 1e-6})
    )

    simulation_type = data.get('simulation_type')

    # need to modify the '*4' to be configurable via post request
    if simulation_type == 'experiment':
        simulation_config = SimulationConfiguration(
            experiment=data.get('experiment', [
                "Discharge at C/5 for 10 hours or until 2.5 V",
                "Rest for 1 hour",
                "Charge at 1 A until 3.5 V",
                "Hold at 3.5 V until 10 mA",
                "Rest for 1 hour",
            ] * 4)
        )
    elif simulation_type == 'time_eval':
        simulation_config = SimulationConfiguration(
            t_eval=data.get('t_eval', [0, 7200])
        )
    elif simulation_type == 'drive_cycle':
        drive_cycle = data.get('drive_cycle')
        simulation_config = SimulationConfiguration(
            drive_cycle=DriveCycleFile(
                chemistry=drive_cycle.get('chemistry', 'NMC'),
                drive_cycle_file=drive_cycle.get('drive_cycle_file', 'NMC_25degC_1C')
            )
        )
    else:
        return jsonify({'error': 'Invalid simulation type'}), 400

    # Initialize the simulation runner
    sim_runner = SimulationRunner(battery_config, solver_config)

    # run simulation
    sim_runner.run_simulation(config=simulation_config)

    # Get the display parameters from the request, default params are below, if not provided
    display_params = data.get('display_params', ["Terminal voltage [V]"])

    # Display the simulation results based on the requested parameters
    results = sim_runner.display_results(display_params)

    return jsonify(results)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8084, debug=True)