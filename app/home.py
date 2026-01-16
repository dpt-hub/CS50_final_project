from flask import Blueprint, render_template, url_for

bp = Blueprint('home', __name__)

@bp.route('/')
def homepage():
    return render_template('home/landing_page.html')

@bp.route('/features')
def features():

    # TODO: Create html file
    return render_template('home/features.html')

@bp.route('/pricing')
def pricing():
    return render_template('home/pricing.html')

@bp.route('/about-us')
def about_us():

    # TODO: Create html file
    return render_template('home/about_us.html')