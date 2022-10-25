import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, '/root/solviing_dashboard')

from flask import Flask

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    #app.config.from_object('config.Config')

    with app.app_context():

        # Import parts of our core Flask app
        import routes

        # Import Dash application
        from app import init_dashboard
        app = init_dashboard(app)

        return app
