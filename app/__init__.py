import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from dotenv import load_dotenv

db = SQLAlchemy()
api = Api()

def create_app():
    load_dotenv()  # Load .env variables

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartkrishi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.vegetable_routes import vegetable_bp
    from app.routes.weather_routes import weather_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(vegetable_bp, url_prefix='/api/vegetables')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')

    @app.route('/')
    def home():
        return '<h1>Welcome to Smart Krishi API</h1>'

    return app
