import pybamm
from pydantic import BaseModel, StrictStr, validator

NMC = r"C:\Users\markv\Documents\Repos\2024\BatterySimulator_v2\BatterySimulator_SimulationBackend\Li-Ion-Battery-Simulator\BatterySimulator\Models\NMC\AE_gen1_BPX.json"
LFP = r"C:\Users\markv\Documents\Repos\2024\BatterySimulator_v2\BatterySimulator_SimulationBackend\Li-Ion-Battery-Simulator\BatterySimulator\Models\LFP\lfp_18650_cell_BPX.json"

class ConfigModel(BaseModel):
    bpx_model: StrictStr 
    electrochemical_model: StrictStr

    # need to make it scalable to more bpx models
    # proposal:
    # dont look for not in dict of strings but if not in file 
    @validator("bpx_model")
    def validate_chemistry(cls, bpx_model):
        if bpx_model not in {"LFP", "NMC"}:
            raise ValueError(f"Invalid BPX Model Type: {bpx_model}. Use LFP or NMC")
        return bpx_model
    
    # need to invesitage if the solver func matters per bpx model. could just make a default one per model with a class instance
    @validator("electrochemical_model")
    def validate_electrochemical_model(cls, electrochemical_model):
        if electrochemical_model not in {"DFN", "SPM", "SPMe"}:
            raise ValueError(f"Invalid Electrochemical Model Type: {electrochemical_model}. Model must be defined as DFN, SPM or SPMe")
        return electrochemical_model
        
    # need to consider removing strictStr and  make it literate of just json files from the config battery chemistries
    # need to consider other properties of design. Will i need custom bpx models users make uploaded to a DB and pulled down or all local?
    # right now everything is hardcoded - how do i give way to the above. e.g. use case, I want to uplaod a custom model, how does that register on the backend to be used
    def set_bpx_model(self):
        if self.bpx_model == "LFP":
            parameter_values = pybamm.ParameterValues.create_from_bpx(LFP)
        elif self.bpx_model == "NMC":
            parameter_values = pybamm.ParameterValues.create_from_bpx(NMC)
        else:
            raise ValueError(f"Invalid BPX Model Type: {self.bpx_model}. Use LFP or NMC")
        
        return parameter_values

def main():
    setup_model = ConfigModel(bpx_model="LFP", electrochemical_model="DFN")
    parameter_values = setup_model.set_bpx_model()

    print(parameter_values)

if __name__ == "__main__":
    main()