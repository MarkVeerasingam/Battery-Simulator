from pydantic import BaseModel
from typing import Dict, List, Optional

class BPXModel(BaseModel):
    name: str
    path: str
    output_results_path: Optional[str] = None

class ChemistryModels(BaseModel):
    models: List[BPXModel]

# A library of all avaible BPX Schema models of their given chemistry
AVAILABLE_BATTERY_MODELS: Dict[str, ChemistryModels] = {
    "NMC": ChemistryModels(models=[
        BPXModel(name="AE_gen1_BPX", path="BatterySimulator/Models/NMC/AE_gen1_BPX.json"),
        BPXModel(name="NMC_Pouch_cell", path="BatterySimulator/Models/NMC/nmc_pouch_cell_BPX.json", output_results_path="BatterySimulator\data\simulation_output/nmc_pouch_cell_BPX_SIMULATION_OUTPUT.json"),
    ]),
    "LFP": ChemistryModels(models=[
        BPXModel(name="lfp_18650_cell_BPX", path="BatterySimulator/Models/LFP/lfp_18650_cell_BPX.json", output_results_path="BatterySimulator\data\simulation_output/lfp_18650_cell_BPX_SIMULATION_OUTPUT.json"),
        BPXModel(name="LFP_model2", path="BatterySimulator/Models/LFP/LFP_model2.json"),
    ]),
}

# re: output_results_path
# The reason for this is beacuse we need to know all the simualtion output parameters for flask to use. - Flask cant pass a whole simulation, so we need to pass entries like Current,Voltage etc.. 
# Since the simulation is computed, the user can choose what simulation outputs they want to see before or after the simulation is executed.
# to do this we need to have a record of all of the simulation.solution[parameters] between the backend and frontend.
# My thought process to access these results for flask for any new uploaded models is...
# When a user uploads a model, the model will run through a mock simulation [(0,3600)] 
# The simulation entry result keys will then be then parsed and formatted into a json.dump()