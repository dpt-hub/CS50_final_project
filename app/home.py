from flask import Blueprint, render_template

bp = Blueprint('home', __name__)

@bp.route('/')
def homepage():
    return render_template('landing_page.html')

@bp.route('/features')
def features():

    # TODO: Create html file
    return render_template('features.html')

@bp.route('/pricing')
def pricing():

    # TODO: Create html file
    return render_template('pricing.html')

@bp.route('/about-us')
def about_us():

    # TODO: Create html file
    return render_template('about_us.html')