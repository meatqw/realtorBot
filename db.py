from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import config

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.DB_LOGIN}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app_root = os.path.dirname(os.path.abspath(__file__))

# DB Model USER
class Users(db.Model):
    id = db.Column(db.String(200), primary_key=True)
    login = db.Column(db.String(200), nullable=True)
    fname = db.Column(db.String(200), nullable=True)
    lname = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Boolean(), nullable=True)
    message_count = db.Column(db.Integer(), nullable=True, default=0)


if __name__ == '__main__':
    db.create_all()
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=5005)
    # Session(app)