from config.Models.PhysicsBasedModel import ElectrochemicalModelConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from App.BatteryModel.PhysicsBasedModels.PhysicsBasedModels import PhysicsBasedModels
from App.BatteryModel.ECM.EquivalentCircuitModel import EquivalentCircuitModel

class ModelRunner:
    @staticmethod
    def create(config: ElectrochemicalModelConfiguration):
        
        # Physics based modelling
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
    
    @staticmethod
    def create_ecm(config: ECMConfiguration):  
        # ECM modelling
        equivalent_circuit_model = config.equivalent_circuit_model
        
        return EquivalentCircuitModel.create_thevenin()
        
        # creating a generic ecm thevenin model with no model options as of right now
        # if equivalent_circuit_model == "ECM":
            # return EquivalentCircuitModel.create_thevenin()
        # else:
        #     raise ValueError(f"Invalid ECM Model Type: {equivalent_circuit_model}") # this should never be raised, by default ecm is a hardcoded thevenin model