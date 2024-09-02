import time
import pybamm
import numpy as np
import jax
import matplotlib.pyplot as plt
import os

# specify 1 logical device for execution
ncpu = 1
os.environ['XLA_FLAGS'] = (
    '--xla_force_host_platform_device_count={}'.format(ncpu)
)

# print out the available devices
print('devices', jax.devices())

pybamm.set_logging_level("INFO")
model = pybamm.lithium_ion.SPM()
model.convert_to_format = "jax"
model.events = []

# create geometry
geometry = model.default_geometry

# load parameter values and process model and geometry
param = model.default_parameter_values
parameter = "Electrode height [m]"
value = param[parameter]
param.update({parameter: "[input]"})
param.process_model(model)
param.process_geometry(geometry)

# set mesh
mesh = pybamm.Mesh(geometry, model.default_submesh_types, model.default_var_pts)

# discretise model
disc = pybamm.Discretisation(mesh, model.default_spatial_methods)
disc.process_model(model)

# solve model for 1 hour
t_eval = np.linspace(0, 3600, 100)
solver = pybamm.JaxSolver()

def solve_model(model, t_eval, inputs):
    return solver.solve(model, t_eval, inputs=inputs)

# Run the initial solution
try:
    solution = solve_model(
        model, t_eval,
        inputs={parameter: value},
    )
except RuntimeError as e:
    print(f"Initial solve failed: {e}")

# Create a new function for parallel execution
def parallel_solve(inputs_array):
    solve_fn = solver.get_solve(model, t_eval)
    return jax.pmap(solve_fn)(inputs_array)

# Prepare inputs for parallel execution
inputs_array = {
    parameter: jax.numpy.linspace(value / 10, value * 10, ncpu)
}

# Execute in parallel
print('running in parallel')
tic = time.perf_counter()
try:
    result_array = parallel_solve(inputs_array)
except RuntimeError as e:
    print(f"Parallel solve failed: {e}")

# Access the result to ensure it's actually computed
print(result_array[0, 0, 0])
toc = time.perf_counter()
print('time elapsed: {} sec'.format(toc - tic))

