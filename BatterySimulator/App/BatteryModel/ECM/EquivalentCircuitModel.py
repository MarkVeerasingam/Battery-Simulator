import pybamm

class EquivalentCircuitModel:
    @staticmethod
    def create_thevenin():
        return pybamm.equivalent_circuit.Thevenin()