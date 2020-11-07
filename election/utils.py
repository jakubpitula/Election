from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.admin == 0:
            flash('Nie masz dostępu do tej strony.', 'danger')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated
