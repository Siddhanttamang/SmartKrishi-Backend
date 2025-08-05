import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta

from app.utils.extensions import login_manager

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

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    CORS(app)

    # Configurations
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')
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
    login_manager.init_app(app)
    login_manager.login_view = 'admin_auth.login'

    from app.models.user import UserModel
    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    # Register API blueprints
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

    # Admin auth blueprint
    from app.admin.admin_auth import admin_auth
    app.register_blueprint(admin_auth)

    # Root
    @app.route('/')
    def home():
        return '<h1>Welcome to Smart Krishi API</h1>'

    # Serve uploaded images
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # ✅ Initialize secure admin panel
    from app.admin import init_admin
    init_admin(app)

    return app
