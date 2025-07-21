from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from .extensions import db, migrate

from .routes.family_route import bp as family_bp
from .routes.auth_route import bp as auth_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(family_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)