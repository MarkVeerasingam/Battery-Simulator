import pybamm
from config.Config import ElectrochemicalModelConfiguration

class ElectrochemicalModel:
    @staticmethod
    def create(config: ElectrochemicalModelConfiguration):
        electrochemical_model = config.electrochemical_model

        options = {"cell geometry": config.cell_geometry, "thermal": config.thermal_model}

        if electrochemical_model == "DFN":
            return pybamm.lithium_ion.DFN(options=options)
        elif electrochemical_model == "SPM":
            return pybamm.lithium_ion.SPM(options=options)
        elif electrochemical_model == "SPMe":
            return pybamm.lithium_ion.SPMe(options=options)
        else:
            raise ValueError(f"Invalid Electrochemical Model Type: {electrochemical_model}")