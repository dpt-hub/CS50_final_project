from .db import get_db
from .auth import login_required

from flask import Blueprint, request, g, url_for, render_template

# Add variables to flask.route
from markupsafe import escape

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
@login_required
def map():
    
    # Fetch user's client database from db
    db = get_db()
    cur = db.cursor()
    clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()

    # TODO: Add client data to map logic (if needed)

    # Render map
    return render_template('main/main.html')


@bp.route('/list')
@login_required
def client_list():

    # Fetch user's client database from db
    db = get_db()
    cur = db.cursor()
    clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', g.user["user_id"]).fetchall()

    # TODO: Add client data to list logic

    return render_template('main/list.html')


@bp.route('/list/<client>', methods=('GET', 'POST'))
@login_required
def single_client(client):
    # Configure a current client variable to be client_id
    g.client = client

    # After user tries to edit client
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Check if user's input is correct
        if not name or not type or not latitude or not longitude:
            flash('Missing required fields.')
        else:
            try:
                float(latitude)
                float(longitude)
            except ValueError:
                flash('Invalid coordinates.')

        # Store user's edit in database.
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute(
                'UPDATE clients SET name = ?, type = ?, lat = ?, lon = ? WHERE client_id = ?',
                name,
                type,
                latitude,
                longitude,
                g.client
            )
            db.commit()
        except db.ProgrammingError:
            flash('Couldn\'t save information.')

    # Load current client information
    db = get_db()
    cur = db.cursor()
    client = cur.execute('SELECT * FROM clients WHERE client_id = ? AND user_id = ?', g.client, g.user['user.id']).fetchone()

    # Check for error in retrieving client info
    if client is None:
        flash('Couldn\'t retrieve client\'s information.')

    return render_template('main/client.html')