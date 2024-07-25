import json
import pybamm

"""This file is temporary until i make something more sophisticated"""

bpx_model = r'C:\Users\markv\Documents\Repos\2024\BatterySimulator_v2\BatterySimulator_SimulationBackend\Li-Ion-Battery-Simulator\BatterySimulator\Models\LFP\lfp_18650_cell_BPX.json'
model = pybamm.lithium_ion.DFN()
parameter_values = pybamm.ParameterValues.create_from_bpx(bpx_model)
simulation = pybamm.Simulation(model=model, parameter_values=parameter_values)
solution = simulation.solve([0,3600])

solution.data.keys()

keys = list(model.variables.keys())

for key in keys:
    print(key)

file_path = r'C:\Users\markv\Desktop\test_dump.json'

data_to_write = {
    "output_data": keys
}

def write_into_json(new_data, filename):
    try:
        with open(filename,'r+') as file:
            json.dump(new_data, file, indent=4)
        print(f"Parameters have been written to {file_path}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

write_into_json(data_to_write, file_path)