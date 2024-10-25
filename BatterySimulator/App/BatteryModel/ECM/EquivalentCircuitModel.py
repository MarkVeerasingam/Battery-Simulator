import pybamm

class EquivalentCircuitModel:
    @staticmethod
    def create_thevenin(options):
        return pybamm.equivalent_circuit.Thevenin(options=options)