from flask import Flask
from LFP.Simulation.LFP_experiment import simulateLFP_experiment_bp
from datetime import datetime
#from flask_sqlalchemy import SQLAlchemy

# create flask instance
app = Flask(__name__)
app.register_blueprint(simulateLFP_experiment_bp, url_prefix='/LFP_experiment')

# # add database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/users'

# # secret key!!
# app.config['SECRET_KEY'] = "my_secret_key"
# # init the db
# db = SQLAlchemy(app)

# # create a model
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)

#     # Create a string
#     def __repr__(self):
#         return '<Name %r>' % self.name

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)