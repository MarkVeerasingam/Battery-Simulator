import time
import json
from api.simulation_endpoints import experiment, time_eval, drive_cycle
from App.Simulation import Simulation

if __name__ == '__main__':
    start_time = time.time()

    # time_eval()
    # experiment()    
    drive_cycle()

    print(f"Time(s): {time.time() - start_time:.2f}")