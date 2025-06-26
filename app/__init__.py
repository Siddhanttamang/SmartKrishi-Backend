import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()

# Enable SQLite foreign key constraints
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    load_dotenv()  # Load .env variables

    app = Flask(__name__)
    CORS(app)

    # Upload folder setup
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists

    # Configurations
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartkrishi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    # Register blueprints
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

    # Root route
    @app.route('/')
    def home():
        return '<h1>Welcome to Smart Krishi API</h1>'

    # Serve uploaded images
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
