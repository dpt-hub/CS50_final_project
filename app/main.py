from .db import get_db
from .auth import login_required

from flask import Blueprint, request, g, url_for, render_template, jsonify, flash, send_from_directory

import json

# Add variables to flask.route
from markupsafe import escape

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def map():
    
    error = None
    if request.method == 'POST':
        name = request.form.get("name")
        type = request.form.get("type")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if not name:
            error = "Client's name required."
        elif not type:
            error = "Client's type required."
        elif not latitude or not longitude:
            error = "Couldn\'t retrieve lat or lon values."
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            # TODO: Change error message after debugging
            error = "Couldn\'t convert lat or lon values to integers."
        
        if error is None:
            db = get_db()
            cur = db.cursor()
            try:
                cur.execute('INSERT INTO clients (user_id, name, type, latitude, longitude) VALUES (?, ?, ?, ?, ?)', 
                (g.user["user_id"], name, type, latitude, longitude))
                db.commit()
            except db.IntegrityError:
                # TODO: Change error message after debugging
                error = 'Couldn\'t insert data to database.'

    if error is not None:
        flash(error)
    # Render map
    return render_template('main/map.html')


@bp.route('/clients', methods=("GET", "POST"))
@login_required
def client_list():
    
    if request.method == 'POST':
        error = None

        # Handling client deletion
        if request.form.get("deleteClient") is not None:
            inputs = request.form.to_dict(True)
            
            if len(inputs) < 2:
                error = "Select at least one client to delete."
            else:
                db = get_db()
                cur = db.cursor()
                count = 0
                for input in inputs:
                    count += 1
                    if input == "deleteClient":
                        print("deleteClient passed")
                    else:
                        print(f"Current count: {count}")
                        print(inputs[input])
                        try:
                            client_id = inputs[input]
                            cur.execute (
                                'DELETE FROM clients WHERE client_id = ? AND user_id = ?',
                                (client_id, g.user["user_id"])
                            )
                            db.commit()
                        except:
                            error = "DEBUG - DELETING DATA ERROR"

        # Handling client creation
        elif request.form.get("createClient") is not None:
            name = request.form.get('name').strip()
            type = request.form.get('type').strip()
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')

            # Check if user's input is correct
            if not name or not type or not latitude or not longitude:
                error = 'Missing required fields.'
            else:
                try:
                    float(latitude)
                    float(longitude)
                except ValueError:
                    error = 'Invalid coordinates.'

            # Store user's edit in database.
            if error is None:
                try:
                    db = get_db()
                    cur = db.cursor()
                    cur.execute(
                        'INSERT INTO clients (user_id, name, type, latitude, longitude) VALUES (?, ?, ?, ?, ?)',
                        (g.user['user_id'], name, type, latitude, longitude)
                    )
                    db.commit()
                except db.IntegrityError:
                    error = 'Couldn\'t save information.'
        
        # Handling no form or evil user interaction with form after POST request
        else:
            error = 'Something went wrong.'
            db = get_db()
            cur = db.cursor()

        if error is not None:
            db = get_db()
            cur = db.cursor()
            columnHeaders = cur.execute('PRAGMA table_info(clients)').fetchall()
            clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()
            flash(error)
            return render_template('main/clients.html', clients=clients, columnHeaders=columnHeaders)
        else:
            columnHeaders = cur.execute('PRAGMA table_info(clients)').fetchall()
            clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()
            return render_template('main/clients.html', clients=clients, columnHeaders=columnHeaders)
    
    else:
        # Fetch user's client database from db
        db = get_db()
        cur = db.cursor()
        columnHeaders = cur.execute('PRAGMA table_info(clients)').fetchall()
        clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()
        # TODO: Add client data to list logic
        return render_template('main/clients.html', clients=clients, columnHeaders=columnHeaders)


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

@bp.route('/fetch/clients')
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

@bp.route('/fetch/logo')
@login_required
def fetch_logo():
    
    return send_from_directory('static', 'images/logo.svg')

@bp.route('/fetch/tempmarker')
@login_required
def fetch_marker():
    
    return send_from_directory('static', 'images/tempmarker.svg')

    