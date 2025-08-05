from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import UserModel
from werkzeug.security import check_password_hash
from passlib.hash import bcrypt


admin_auth = Blueprint('admin_auth', __name__, url_prefix='/') 


@admin_auth.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserModel.query.filter_by(email=email).first()
        if user and bcrypt.verify(password, user.password) and user.role == 'admin':

            login_user(user)
            return redirect('/admin/users')
        flash("Invalid credentials or not an admin")
    return render_template('admin/login.html')

@admin_auth.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
