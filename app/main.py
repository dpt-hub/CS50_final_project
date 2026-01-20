from .db import get_db
from .auth import login_required

from flask import Blueprint, request, g, url_for, render_template, jsonify

import json

# Add variables to flask.route
from markupsafe import escape

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/')
@login_required
def map():
    
    # Render map
    return render_template('main/map.html')


@bp.route('/clients')
@login_required
def client_list():

    # TODO: Add client data to list logic

    return render_template('main/clients.html')


@bp.route('/clients/<client>', methods=('GET', 'POST'))
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
    client = cur.execute('SELECT * FROM clients WHERE client_id = ? AND user_id = ?', (g.client, g.user['user.id'])).fetchone()

    # Check for error in retrieving client info
    if client is None:
        flash('Couldn\'t retrieve client\'s information.')

    return render_template('main/client.html')

@bp.route('/reports')
@login_required
def reports():

    # TODO: Add client data to list logic

    return render_template('main/reports.html')

@bp.route('/fetch-clients')
@login_required
def fetch_clients():
    # Fetch user's client database from db
    db = get_db()
    cur = db.cursor()
    clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()

    # Render clients into json to be processed by javascript code
    temp = []
    for client in clients:
        name = client["name"]
        type = client["type"]
        latitude = client["latitude"]
        longitude = client["longitude"]
        temp.append({
            "name": name,
            "type": type,
            "latitude": latitude,
            "longitude": longitude
            })
        
    return jsonify(temp)

@bp.route('/create-client/<marker>')
@login_required
def create_clients(marker):
    # Fetch user's client database from db
    new_client = json.load(marker)
    db = get_db()
    cur = db.cursor()
    error = None
    try:
        name = new_client["name"]
        type = new_client["type"]
        latitude = new_client["latitude"]
        longitude = new_client["longitude"]
        cur.execute('INSERT INTO clients (user_id, name, type, latitude, longitude) VALUES (?, ?, ?, ?, ?)', 
        (g.user["user_id"], name, type, latitude, longitude))
        db.commit()
    except db.IntegrityError:
        error = 'Something went wrong.'

    if error is not None:
        flash(error)