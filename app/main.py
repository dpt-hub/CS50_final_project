from .db import get_db
from .auth import login_required
from flask import Blueprint, request, g, url_for, render_template, jsonify, flash, send_from_directory, redirect, abort
import werkzeug
import json
# Add variables to flask.route
from markupsafe import escape
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def map():
    
    error = None
    if request.method == 'POST':
        name = request.form.get("name")
        type = request.form.get("type")
        address = request.form.get("address")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        if not name or not type or not address or not latitude or not longitude:
            error = "Missing required fields."
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            # TODO: Change error message after debugging
            error = "Invalid coordinate format. Latitude and longitude must be numbers."
        
        if error is None:
            db = get_db()
            cur = db.cursor()
            try:
                cur.execute('INSERT INTO clients (user_id, name, type, address, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)', 
                (g.user["user_id"], name, type, address, latitude, longitude))
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
                    if input not in ("deleteClient"):
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
            address = request.form.get('address').strip()
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')

            # Check if user's input is correct
            if not name or not type or not address or not latitude or not longitude:
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
                        'INSERT INTO clients (user_id, name, type, address, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)',
                        (g.user['user_id'], name, type, address, latitude, longitude)
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
            flash(error)

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
        name = request.form.get('name').strip()
        type = request.form.get('type').strip()
        address = request.form.get('address').strip()
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        error = None

        # Check if user's input is correct
        if not name or not type or not address or not latitude or not longitude:
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
                    'UPDATE clients SET name = ?, type = ?, address = ?, latitude = ?, longitude = ? WHERE client_id = ?',
                    (name, type, address, latitude, longitude, client_id)
                )
                db.commit()
            except db.ProgrammingError:
                error = 'Something went wrong.'
        
        if error is None:
            return redirect(url_for('main.client_list'))
        else:
            flash(error)

    return render_template('main/client.html', client=client, columnHeaders=columnHeaders)

@bp.route('/reports', methods=("GET", "POST"))
@login_required
def reports():

    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        error = None

        # Handling visit deletion
        if request.form.get("deleteVisit") is not None:
            inputs = request.form.to_dict(True)
            
            if len(inputs) < 2:
                error = "Select at least one visit to delete."
            else:
                count = 0
                for input in inputs:
                    count += 1
                    if input not in ("visitClient"):
                        try:
                            visit_id = inputs[input]
                            cur.execute (
                                'DELETE FROM visits WHERE visit_id = ? AND client_id IN (SELECT client_id FROM clients WHERE user_id = ?)',
                                (visit_id, g.user["user_id"])
                            )
                            db.commit()
                        except:
                            error = "DEBUG - DELETING DATA ERROR"

        # Handling client creation
        elif request.form.get("addVisit") is not None:
            client_id = request.form.get("client_id")
            date = request.form.get("date")
            order_value = request.form.get("order_value")

            # Check if user's input is correct
            if not client_id or not date or not order_value:
                error = 'Missing required fields.'
            else:
                try:
                    float(order_value)
                except ValueError:
                    error = 'Invalid order value.'

            if error is None:
                try:
                    date = datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    error = 'Invalid date format.'

            # Store user's edit in database.
            if error is None:
                # Check if client_id is from user (SECURITY MUST)
                    isClient = cur.execute(
                                'SELECT * FROM clients WHERE user_id = ? AND client_id = ?',
                                (g.user['user_id'], client_id)
                                ).fetchone()
                    if isClient is None:
                        error = 'Invalid client association. Visit could not be recorded.'
                    else:
                        try:
                            cur.execute(
                                'INSERT INTO visits (client_id, date, order_value) VALUES (?, ?, ?)',
                                (client_id, date, order_value)
                            )
                            db.commit()
                        except db.IntegrityError:
                            error = 'Couldn\'t save information.'
        
        # Handling no form or evil user interaction with form after POST request
        else:
            error = 'Something went wrong.'

        if error is not None:
            flash(error)

        visits = cur.execute(
            'SELECT * FROM visits WHERE client_id IN (SELECT client_id FROM clients WHERE user_id = ?)',
            (g.user["user_id"],)
            ).fetchall()
        columnHeaders = cur.execute('PRAGMA table_info(visits)').fetchall()
        clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()
        return render_template('main/reports.html', visits=visits, clients=clients, columnHeaders=columnHeaders)

    db = get_db()
    cur = db.cursor()
    columnHeaders = cur.execute('PRAGMA table_info(visits)').fetchall()
    clients = cur.execute('SELECT * FROM clients WHERE user_id = ?', (g.user["user_id"],)).fetchall()
    visits = cur.execute(
        'SELECT * FROM visits WHERE client_id IN (SELECT client_id FROM clients WHERE user_id = ?)',
        (g.user["user_id"],)
        ).fetchall()
    return render_template('main/reports.html', visits=visits, clients=clients, columnHeaders=columnHeaders)

@bp.route('/reports/<visit_id>', methods=('GET', 'POST'))
@login_required
def single_visit(visit_id):
        
    # Check if visit_id is related to current user_id (SECURITY MUST)
    db = get_db()
    cur = db.cursor()
    columnHeaders = cur.execute('PRAGMA table_info(visits)').fetchall()
    clients = cur.execute(
        'SELECT * FROM clients WHERE user_id = ?',
        (g.user['user_id'],)
    ).fetchall()
    visit = cur.execute(
        'SELECT * FROM visits WHERE visit_id = ? AND client_id IN (SELECT client_id FROM clients WHERE user_id = ?)',
        (visit_id, g.user['user_id'])
    ).fetchone()

    if visit is None or clients is None:
        abort(404)

    # After user tries to edit client
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        date = request.form.get('date')
        order_value = request.form.get('order_value')
        error = None

        # Check if user's input is correct
        if not client_id or not date or not order_value:
            error = 'Missing required fields.'
        else:
            try:
                float(order_value)
            except ValueError:
                error = 'Invalid order value.'

        # Check if client_id belongs to current user (SECURITY MUST)
        if error is None:
            client = cur.execute(
                'SELECT * FROM clients WHERE client_id = ? AND user_id = ?',
                (client_id, g.user['user_id'])
            ).fetchone()
            if client is None:
                error = 'Invalid selected client.'

        if error is None:
            try:
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                error = 'Invalid date format.'

        # Store user's edit in database.
        if error is None:
            try:
                cur.execute(
                    'UPDATE visits SET client_id = ?, date = ?, order_value = ? WHERE visit_id = ?',
                    (client_id, date, order_value, visit_id)
                )
                db.commit()
            except db.ProgrammingError:
                error = 'Something went wrong.'
        
        if error is None:
            return redirect(url_for('main.reports'))
        else:
            flash(error)

    return render_template('main/visit.html', visit=visit, clients=clients, columnHeaders=columnHeaders)

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
    unwanted_columns = ("client_id", "user_id")
    for client in clients:
        tempDict = {}
        for column in columnHeaders:
            if column["name"] not in unwanted_columns:
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