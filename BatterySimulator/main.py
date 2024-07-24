import time
from api.simulation_endpoints import experiment, time_eval, drive_cycle
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    start_time = time.time()

    time_eval()
    experiment()    
    drive_cycle()

    # @app.route('/experiment')
    # def run_simulation():
    #     return experiment()
    
    # app.run(debug=True, host="0.0.0.0", port=8084)

    print(f"Time(s): {time.time() - start_time:.2f}")