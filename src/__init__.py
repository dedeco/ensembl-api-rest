import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache()


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    CORS(app,
         supports_credentials=True,
         resources={r"*": {"origins": app.config['INDEX_URL']}}
         )
    sentry_sdk.init(
        dsn=app.config['SENTRY_URL'],
        integrations=[FlaskIntegration()]
    )
    cache.init_app(app, config={'CACHE_TYPE': 'simple',
                                'CACHE_DEFAULT_TIMEOUT': app.config['TIMEOUT_CACHE']})


import src.gene


def register_blueprints(app):
    app.register_blueprint(src.gene.gene_blueprint, url_prefix='/api/v1')
