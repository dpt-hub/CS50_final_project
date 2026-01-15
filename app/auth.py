from .db import get_db
# Imports sqlite3 aswell

from flask import Blueprint, route, request, render_template

import werkzeug.security

bp = Blueprint('auth', __name__, url_prefix='/auth' )


@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username:
            flash('Username required.')
        elif not password or not confirm_password:
            flash('Password required.')
        elif password != confirm_password:
            flash('Matching passwords required.')

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
            flash('Username already taken.')

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username:
            flash('Username required.')
        elif not password:
            flash('Password required.')

        db = get_db()
        cur = db.cursor()
        res = cur.execute('SELECT * FROM users WHERE username = ?', username)

        if res.fetchone() is None:

            # TODO: Change error message to give out less information to user (Debugging Mode)

            flash('Incorrect username.')
        elif not check_password_hash(res["password"], password):

            # TODO: Change error message to give out less information to user (Debugging Mode)

            flash('Incorrect password.')
        else:

            # TODO: Redirect to main application
            
            return 0
    
    return render_template('auth/login.html')
        
