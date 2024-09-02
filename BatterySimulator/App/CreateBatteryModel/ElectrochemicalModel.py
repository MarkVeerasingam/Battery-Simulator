import pybamm
from config.Config import ElectrochemicalConfiguration

class ElectrochemicalModel:
    @staticmethod
    def create(config: ElectrochemicalConfiguration):
        electrochemical_model = config.electrochemical_model

        options = {"cell geometry": config.cell_geometry, "thermal": config.thermal_model}

        if electrochemical_model == "DFN":
            return pybamm.lithium_ion.DFN(options=options)
        elif electrochemical_model == "SPM":
            return pybamm.lithium_ion.SPM()
        elif electrochemical_model == "SPMe":
            return pybamm.lithium_ion.SPMe()
        else:
            raise ValueError(f"Invalid Electrochemical Model Type: {electrochemical_model}")