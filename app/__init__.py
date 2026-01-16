import os

from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='TOFILL',
        DATABASE=os.path.join(app.instance_path, 'TOFILL.db')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import close_db
    app.teardown_appcontext(close_db)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)

    from . import home
    app.register_blueprint(home.py)

    return app

