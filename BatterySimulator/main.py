import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask
from LFP.Simulation.LFP_experiment import simulateLFP_experiment_bp
from datetime import datetime

# create flask instance
app = Flask(__name__)
app.register_blueprint(simulateLFP_experiment_bp, url_prefix='/LFP_experiment')

# Database
# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)