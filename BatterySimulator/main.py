from flask import Flask
from Simulation.SingleCell_Experiment import bp_LFP_experiment

# create flask instance
app = Flask(__name__)
app.register_blueprint(bp_LFP_experiment, url_prefix='/LFP/singleCell')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)