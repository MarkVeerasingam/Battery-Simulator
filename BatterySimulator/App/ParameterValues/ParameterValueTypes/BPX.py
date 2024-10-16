import pybamm
from libraries.CellLibrary import AVAILABLE_BPX_BATTERY_MODELS

class BPXParameterValues:
    @staticmethod
    def create(parameter_value: str):
        # Look for availble BPX Parameter Value JSON files
        parameter_values = next((m for m in AVAILABLE_BPX_BATTERY_MODELS if m.name == parameter_value), None)

        if parameter_values is None:
            raise ValueError(f"Invalid BPX model: {parameter_value}. Available models: {[m.name for m in AVAILABLE_BPX_BATTERY_MODELS]}")

        # Create parameter values from BPX path
        return pybamm.ParameterValues.create_from_bpx(parameter_value.path)