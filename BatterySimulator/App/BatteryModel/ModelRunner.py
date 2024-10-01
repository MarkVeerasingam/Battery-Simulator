from config.Config import ElectrochemicalModelConfiguration
from App.BatteryModel.PhysicsBasedModels.PhysicsBasedModels import PhysicsBasedModels

class ModelRunner:
    @staticmethod
    def create(config: ElectrochemicalModelConfiguration):
        electrochemical_model = config.electrochemical_model

        options = {"cell geometry": config.cell_geometry, "thermal": config.thermal_model}

        if electrochemical_model == "DFN":
            return PhysicsBasedModels.create_dfn(options)
        elif electrochemical_model == "SPM":
            return PhysicsBasedModels.create_spm(options)
        elif electrochemical_model == "SPMe":
            return PhysicsBasedModels.create_spme(options)
        else:
            raise ValueError(f"Invalid Electrochemical Model Type: {electrochemical_model}")