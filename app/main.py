from .db import get_db
from .auth import login_required

from flask import Blueprint, request, g, url_for, render_template, jsonify, flash, send_from_directory, redirect, abort

import werkzeug
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
        print(clients[1]["client_id"])
        # TODO: Add client data to list logic
        return render_template('main/clients.html', clients=clients, columnHeaders=columnHeaders)


@bp.route('/clients/<client_id>', methods=('GET', 'POST'))
@login_required
def single_client(client_id):
    
    # Check if client_id is related to current user_id (SECURITY MUST)
    db = get_db()
    cur = db.cursor()
    columnHeaders = cur.execute('PRAGMA table_info(clients)').fetchall()
    client = cur.execute(
        'SELECT * FROM clients WHERE client_id = ? AND user_id = ?',
        (client_id, g.user["user_id"])
    ).fetchone()

    if client is None:
        abort(404)

    # After user tries to edit client
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        error = None

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
                cur.execute(
                    'UPDATE clients SET name = ?, type = ?, latitude = ?, longitude = ? WHERE client_id = ?',
                    (name, type, latitude, longitude, client_id)
                )
                db.commit()
            except db.ProgrammingError:
                error = 'Something went wrong.'
        
        if error is None:
            return redirect(url_for('main.client_list'))
        else:
            flash(error)

    return render_template('main/client.html', client=client, columnHeaders=columnHeaders)

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
    columnHeaders = cur.execute('PRAGMA table_info(clients)').fetchall()
    clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()

    # Render clients into json to be processed by javascript code
    tempList = []
        for client in clients:
            tempDict = {}
            for column in columnHeaders:
                if not column["name"] == "client_id" or not column["name"] == "user_id":
                    tempDict[column["name"]] = client[column["name"]] 
            tempList.append(tempDict)
            
    return jsonify(tempList)

@bp.route('/fetch/logo')
@login_required
def fetch_logo():
    
    return send_from_directory('static', 'images/logo.svg')

@bp.route('/fetch/tempmarker')
@login_required
def fetch_marker():
    
    return send_from_directory('static', 'images/tempmarker.svg')


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('main/404.html'), 404