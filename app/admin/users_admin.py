from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField, SelectField
from passlib.hash import bcrypt
from app.admin.SecureModelView import SecureModelView

class UserAdmin(SecureModelView):
    form_overrides = {
        'role': SelectField
    }

    form_args = {
        'role': {
            'label': 'Role',
            'choices': [('user', 'User'), ('admin', 'Admin')],
            'coerce': str
        }
    }

    form_extra_fields = {
        'password': PasswordField('Password')
    }

    column_list = ['id', 'name', 'email', 'role', 'address', 'contact']
    form_excluded_columns = ['vegetables', 'reports']

    column_searchable_list = ['name', 'email', 'role']
    column_filters = ['role']

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = bcrypt.hash(form.password.data)
