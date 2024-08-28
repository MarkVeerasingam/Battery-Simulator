from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from config.Config import BatteryConfiguration, ElectrochemicalConfiguration, SolverConfiguration, DriveCycleFile, SimulationConfiguration
from App.SimulationRunner import SimulationRunner
import pybamm

app = Flask(__name__)
CORS(app)

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json

        battery_config = BatteryConfiguration(
            battery_chemistry=data.get('battery_chemistry', 'NMC'),
            bpx_battery_models=data.get('bpx_battery_models', 'NMC_Pouch_cell'),
        )

        electrochemical_config = ElectrochemicalConfiguration(
            electrochemical_model=data.get('electrochemical_model', 'DFN'),
            cell_geometry=data.get('cell_geometry', 'arbitrary'),
            thermal_model=data.get('thermal_model', 'isothermal')
        )

        solver_config = SolverConfiguration(
            solver=data.get('solver', 'CasadiSolver'),
            tolerance=data.get('tolerance', {"atol": 1e-6, "rtol": 1e-6})
        )

        simulation = data.get('simulation', {})
        simulation_type = simulation.get('type')

        if simulation_type == 'drive_cycle':
            drive_cycle = simulation.get('drive_cycle', {})
            simulation_config = SimulationConfiguration(
                drive_cycle=DriveCycleFile(
                    drive_cycle_file=drive_cycle.get('drive_cycle_file', 'NMC_25degC_1C')
                )
            )
        elif simulation_type == 'experiment':
            conditions = simulation.get('experiment', {}).get('conditions', [
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
            conditions = simulation.get('time_eval', {}).get('conditions', [0, 7200])
            simulation_config = SimulationConfiguration(
                t_eval=conditions
            )
        else:
            return jsonify({'error': 'Invalid simulation type'}), 400

        # Initialize the simulation runner
        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)

        # Run simulation
        sim_runner.run_simulation(config=simulation_config)

        # Get the display parameters from the request, default params are below, if not provided
        display_params = data.get('display_params', ["Terminal voltage [V]"])

        # Display the simulation results based on the requested parameters
        results = sim_runner.display_results(display_params)

        return jsonify(results)

    except pybamm.SolverError as e:
        error_message = {'error': str(e)}
        response = make_response(jsonify(error_message), 500)
        return response

    except Exception as e:
        error_message = {'error': f"An unexpected error occurred: {str(e)}"}
        response = make_response(jsonify(error_message), 500)
        return response


if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8084, debug=True)