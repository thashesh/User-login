import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    
    from user_app.app import api_bp
    app.register_blueprint(api_bp, url_prefix='/user_api')

    from user_app.models import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)