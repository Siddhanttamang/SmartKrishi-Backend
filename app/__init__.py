import os
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from dotenv import load_dotenv
from flask import send_from_directory
from flask_migrate import Migrate

migrate = Migrate()
db = SQLAlchemy()
api = Api()
jwt = JWTManager()



def create_app():
    load_dotenv()  # Load .env variables

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartkrishi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = 'uploads'


    db.init_app(app) 
    migrate.init_app(app, db)

    api.init_app(app)
    jwt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.vegetable_routes import vegetable_bp
    from app.routes.weather_routes import weather_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.report_routes import report_bp
    from app.routes.news_routes import news_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(vegetable_bp, url_prefix='/api/vegetables')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(report_bp, url_prefix='/api')
    app.register_blueprint(news_bp, url_prefix='/api')


    @app.route('/')
    def home():
        return '<h1>Welcome to Smart Krishi API</h1>'
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory('uploads', filename)
    return app
