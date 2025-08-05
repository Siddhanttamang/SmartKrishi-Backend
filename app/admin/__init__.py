from flask_admin import Admin
from app.admin.MyAdminIndexView import MyAdminIndexView
from app.admin.SecureModelView import SecureModelView
from app.admin.news_admin import NewsAdmin
from app.admin.vegetables_admin import VegetableAdmin
from app.admin.users_admin import UserAdmin
from app.admin.reports_admin import ReportAdmin

from app.models.user import UserModel
from app.models.vegetable import VegetableModel
from app.models.news import NewsModel
from app.models.report import ReportModel
from app import db

# Single secure admin instance
admin = Admin(
    name="SmartKrishi Admin",
    index_view=MyAdminIndexView(url='/admin'),
    template_mode='bootstrap4',
    endpoint='admin'
)

def init_admin(app):
    admin.init_app(app)

    # Register secure model views
    admin.add_view(UserAdmin(UserModel, db.session, name='Users', endpoint='users'))
    admin.add_view(VegetableAdmin(VegetableModel, db.session, name='Vegetables', endpoint='vegetables'))
    admin.add_view(NewsAdmin(NewsModel, db.session, name='News', endpoint='news'))
    admin.add_view(ReportAdmin(ReportModel, db.session, name='Reports', endpoint='reports'))