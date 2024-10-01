from config.Solver import SolverConfiguration
from App.Solvers.SolverTypes.CasadiSolver import CasadiSolver
from App.Solvers.SolverTypes.IDAKLUSolver import IDAKLUSolver

class SolverRunner:        
    @staticmethod
    def create(config: SolverConfiguration):
        solver_type = config.solver
        
        if solver_type == "CasadiSolver":
            return CasadiSolver.create_casadi_solver(config)
        elif solver_type == "IDAKLUSolver":
            return IDAKLUSolver.create_idaklu_solver(config)
        else:
            raise ValueError("Invalid solver, must be 'CasadiSolver' or 'IDAKLUSolver'")