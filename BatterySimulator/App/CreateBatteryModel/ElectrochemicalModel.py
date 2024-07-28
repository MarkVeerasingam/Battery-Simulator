import pybamm
from config.Config import BatteryConfiguration

class ElectrochemicalModel:
    @staticmethod
    def create(config: BatteryConfiguration):
        electrochemical_model = config.electrochemical_model

        if electrochemical_model == "DFN":
            return pybamm.lithium_ion.DFN()
        elif electrochemical_model == "SPM":
            return pybamm.lithium_ion.SPM()
        elif electrochemical_model == "SPMe":
            return pybamm.lithium_ion.SPMe()
        else:
            raise ValueError(f"Invalid Electrochemical Model Type: {electrochemical_model}")