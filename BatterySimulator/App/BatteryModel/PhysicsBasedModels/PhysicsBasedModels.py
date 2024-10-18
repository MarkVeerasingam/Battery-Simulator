import pybamm

class PhysicsBasedModels:
    @staticmethod
    def create_dfn(options):
        return pybamm.lithium_ion.DFN(options=options)

    @staticmethod
    def create_spm(options):
        return pybamm.lithium_ion.SPM(options=options)

    @staticmethod
    def create_spme(options):
        return pybamm.lithium_ion.SPMe(options=options)
