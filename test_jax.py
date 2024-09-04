import pybamm
import numpy as np

# Initialize the DFN model and configure for JAX
model = pybamm.lithium_ion.DFN()
model.convert_to_format = 'jax'
model.events = []  # Remove events as they're not supported in JAX

# Set up geometry and parameters
geometry = model.default_geometry
param = model.default_parameter_values
param.update({"Current function [A]": "[input]"})
param.process_geometry(geometry)
param.process_model(model)

# Define mesh and discretize the model
n = 10
k = 5
var = pybamm.standard_spatial_vars
var_pts = {var.x_n: n, var.x_s: n, var.x_p: n, var.r_n: k, var.r_p: k}
mesh = pybamm.Mesh(geometry, model.default_submesh_types, var_pts)
disc = pybamm.Discretisation(mesh, model.default_spatial_methods)
disc.process_model(model)

# Define time evaluation points
t_eval = np.linspace(0, 3600, 100)

# Initialize the JAX solver
solver = pybamm.JaxSolver(atol=1e-6, rtol=1e-6, method="BDF")

# Prepare inputs for parameter sweeps
values = np.linspace(0.1, 0.5, 100)
inputs = [{"Current function [A]": value} for value in values]

# Ensure JAX is using GPU if available
import jax
print("Available devices:", jax.devices())

# Solve the model for multiple inputs using GPU acceleration or multithreading
solutions = []
for input_value in values:
    try:
        # Solve the model for the current input value
        solution = solver.solve(model, t_eval, inputs={"Current function [A]": input_value})
        solutions.append(solution)
    except Exception as e:
        print(f"Error solving model for input {input_value}: {e}")

# Process solutions (example: print the final time step of the last solution)
if solutions:
    final_solution = solutions[-1]
    if final_solution:
        print("Final solution at last time step:", final_solution['y'][-1])
else:
    print("No solutions were computed.")
