from flask_admin import Admin
from app.models.news import NewsModel
from app.models.vegetable import VegetableModel
from app.admin.news_admin import NewsAdmin
from app.admin.vegetables_admin import VegetableAdmin
from app import db

admin = Admin(name="SmartKrishi Admin", template_mode='bootstrap4')

def init_admin(app):
    admin.init_app(app)
    admin.add_view(NewsAdmin(NewsModel, db.session))
    admin.add_view(VegetableAdmin(VegetableModel, db.session))
