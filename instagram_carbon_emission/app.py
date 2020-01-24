from flask import Flask
from flask.ext.cors import CORS, cross_origin

from instagram_carbon_emission import auth, api
from instagram_carbon_emission.extensions import db, jwt, migrate, apispec


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask("instagram_carbon_emission", static_folder="./static")
    app.config.from_object("instagram_carbon_emission.config")

    if testing is True:
        app.config["TESTING"] = True

    CORS(
        app,
        resources={
            r"/api/": {
                "origins": "https://instagram-carbon-emission.s3.eu-west-3.amazonaws.com/index.html",
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "Access-Control-Allow-Credentials",
                ],
                "supports_credentials": True,
            }
        },
    )
    configure_extensions(app, cli)
    configure_apispec(app)
    register_blueprints(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT",}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
