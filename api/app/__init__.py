from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "mysql+pymysql://root:123456@localhost/heart_disease_db?charset=utf8mb4"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "secret"

    db.init_app(app)

    CORS(app, origins=["http://localhost:3000"])

    return app