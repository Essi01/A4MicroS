from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    mongo.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .routes import course_blueprint
        # Register Blueprints
        app.register_blueprint(course_blueprint)

        return app
