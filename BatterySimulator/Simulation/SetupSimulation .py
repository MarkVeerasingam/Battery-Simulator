class SetupSimulaton:
    def __init__(self, chemistry, model, solver) -> None:
        self.chemistry = chemistry
        self.params = {}
        self.model = model
        self.solver = solver
        # could put cell_type to help filter dupe chemistries?

    ADJUSTABLE_PARAMETERS = [
            "Ambient temperature [K]",
            "Initial temperature [K]",
            "Lower voltage cut-off [V]",
            "Upper voltage cut-off [V]",
            "Current function [A]",
        ]
    
    # user adjusted paramterValues from base model: 
    def set_model_parameterValues(self, adjusted_paramVals):
        

