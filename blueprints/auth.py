from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_user, login_required, logout_user

from blog.extensions import db, login_manager
from blog.models import Admin

auth_bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return Admin().get(user_id)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    args = request.get_json()
    username, password = args.get('username', ''), args.get('password', '')
    hashed = Admin().hash_password(password)
    user =  db.session.query(Admin).filter_by(username=username, password_hash=hashed).first()
    if user:
        login_user(user)
        flash('Logged in successfully.')
        return 'Logged in!'


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))