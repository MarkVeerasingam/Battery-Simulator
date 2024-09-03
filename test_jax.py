import pybamm
import numpy as np

model = pybamm.lithium_ion.DFN()
model.convert_to_format = 'jax'
model.events = []  # remove events (not supported in jax)
geometry = model.default_geometry
param = model.default_parameter_values
param.update({"Current function [A]": "[input]"})
param.process_geometry(geometry)
param.process_model(model)

n = 10
k = 5
values = np.linspace(0.1, 0.5, 100)
var = pybamm.standard_spatial_vars
var_pts = {var.x_n: n, var.x_s: n, var.x_p: n, var.r_n: k, var.r_p: k}
mesh = pybamm.Mesh(geometry, model.default_submesh_types, var_pts)
disc = pybamm.Discretisation(mesh, model.default_spatial_methods)
disc.process_model(model)
t_eval = np.linspace(0, 3600, 100)
solver = pybamm.JaxSolver(atol=1e-6, rtol=1e-6, method="BDF")
inputs = [{"Current function [A]": value} for value in values]
solution = solver.solve(model, t_eval, inputs=inputs)