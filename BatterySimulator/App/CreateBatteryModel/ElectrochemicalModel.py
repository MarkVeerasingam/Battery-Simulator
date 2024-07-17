import pybamm

class ElectrochemicalModel:
    @staticmethod
    def create(model_type: str):
        if model_type == "DFN":
            return pybamm.lithium_ion.DFN()
        elif model_type == "SPM":
            return pybamm.lithium_ion.SPM()
        elif model_type == "SPMe":
            return pybamm.lithium_ion.SPMe()
        else:
            raise ValueError(f"Invalid Electrochemical Model Type: {model_type}")