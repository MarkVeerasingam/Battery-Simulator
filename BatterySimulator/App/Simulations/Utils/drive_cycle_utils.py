import pandas as pd
from libraries.DriveCycleLibrary import AVAILABLE_DRIVE_CYCLES

def read_drive_cycle_data(drive_cycle_name: str):
    """Read drive cycle data from a CSV file based on the drive cycle name."""
    selected_drive_cycle = next(
        (dc for dc in AVAILABLE_DRIVE_CYCLES if dc.name == drive_cycle_name), 
        None
    )
    if selected_drive_cycle is None:
        raise ValueError(f"Invalid drive cycle name: {drive_cycle_name}.")

    file_path = selected_drive_cycle.path
    if not file_path:
        raise ValueError("Drive cycle file path is empty.")

    try:
        data = pd.read_csv(file_path, comment="#").to_numpy()
        time_data = data[:, 0] 
        current_data = data[:, 1]
        return time_data, current_data
    except FileNotFoundError:
        raise ValueError(f"Drive cycle file '{file_path}' not found.")
    except Exception as e:
        raise ValueError(f"An error occurred while reading the drive cycle file: {str(e)}") 

def interpolate_drive_cycle_data(time_data, current_data):
    """Interpolate the current data from the drive cycle."""
    import pybamm
    return pybamm.Interpolant(time_data, -current_data, pybamm.t, interpolator="linear")