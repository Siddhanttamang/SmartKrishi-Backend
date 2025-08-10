from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from passlib.hash import bcrypt


class UserAdmin(ModelView):
    form_excluded_columns = ('role', 'vegetables', 'reports')

    form_extra_fields = {
        'name': StringField('Name', validators=[DataRequired()]),
        'email': StringField('Email', validators=[DataRequired(), Email()]),
        'contact': StringField('Contact'),
        'password': PasswordField('Password', validators=[DataRequired()])
    }


    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = bcrypt.hash(form.password.data)
        if is_created:
            model.role = 'user'

