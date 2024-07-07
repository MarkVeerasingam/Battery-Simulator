from flask import Flask
from LFP.Simulation.LFP_experiment import simulateLFP_experiment_bp

app = Flask(__name__)
app.register_blueprint(simulateLFP_experiment_bp, url_prefix='/LFP_experiment')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)