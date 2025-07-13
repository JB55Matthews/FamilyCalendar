from flask import Flask
from .config import DevelopmentConfig
from .extensions import db, migrate, jwt

from .routes.family_route import bp as family_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(family_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)