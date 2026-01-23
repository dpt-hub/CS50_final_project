from .db import get_db
from flask import Blueprint, g, request, render_template, flash, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import functools
import re

bp = Blueprint('auth', __name__, url_prefix='/auth' )


@bp.route('/register', methods=['GET', 'POST'])
def register():

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            security_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#?!@$%^&*-])[A-Za-z\d#?!@$%^&*-]{8,64}$"
            pattern = re.compile(security_regex)
            m = re.search(pattern, password)
            error = None

            if not email:
                error = 'Email required.'
            elif not password or not confirm_password:
                error = 'Password required.'
            elif password != confirm_password:
                error = 'Matching passwords required.'
            elif len(password) < 8 or not m:
                error = 'Password does not meet the minimum security requirements.'

            if error:
                flash(error)
                return render_template('auth/register.html')

            db = get_db()
            cur = db.cursor()
            try:
                cur.execute(
                    'INSERT INTO users (email, hashed_password) VALUES (?, ?)',
                    (email, generate_password_hash(password))
                )
                db.commit()
                return redirect(url_for('auth.login'))

            except db.IntegrityError:
                error = 'Email already taken.'

            if error is None:
                return redirect(url_for('auth.login'))

            flash(error)
        return render_template('auth/register.html')
            


@bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        if not email:
            error = 'Email required.'
        elif not password:
            error = 'Password required'

        db = get_db()
        cur = db.cursor()
        res = cur.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if res is None:

            error = 'Incorrect email or password.'
        elif not check_password_hash(res['hashed_password'], password):

            error = 'Incorrect email or password'

        if error is None:
            session.clear()
            session['user_id'] = res['user_id']
            return redirect(url_for('main.map'))
        
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view
