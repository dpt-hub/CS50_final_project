from .db import get_db

from flask import Blueprint, g, request, render_template, flash, session, redirect, url_for

import werkzeug.security
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth' )


@bp.route('/register', methods=['GET', 'POST'])
def register():

    if g.user is None: 

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if not username:
                error = 'Username required.'
            elif not password or not confirm_password:
                error = 'Password required.'
            elif password != confirm_password:
                error = 'Matching passwords required.'

            db = get_db()
            cur = db.cursor()
            try:
                cur.execute(
                    'INSERT INTO users (username, hashed_password) VALUES (?, ?)',
                    username,
                    generate_password_hash(password)
                )
                db.commit()
                return redirect(url_for('auth.login'))

            except db.IntegrityError:
                error:'Username already taken.'

        flash(error)
        
        return render_template('auth/register.html')
    
    else:

        return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            error = 'Username required.'
        elif not password:
            error = 'Password required'

        db = get_db()
        cur = db.cursor()
        res = cur.execute('SELECT * FROM users WHERE username = ?', username).fetchone()

        if res is None:

            # TODO: Change error message to give out less information to user (Debugging Mode)

            error = 'Incorrect username.'
        elif not check_password_hash(res["password"], password):

            # TODO: Change error message to give out less information to user (Debugging Mode)

            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = res['user_id']
            return redirect(url_for('main'))
        
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', user_id).fetchone()

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
