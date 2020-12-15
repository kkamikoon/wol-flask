import os, random

# Cache
from app.cache import cache

# Utilities
from app.utils import (
    get_config,
    set_config
)

# Flask ReCaptcha
from flask_recaptcha import  ReCaptcha

from app.utils.initialization   import (
    init_template_globals,
    init_request_processors
)

# SQLAlchemy && Migrations
from sqlalchemy                 import create_engine 
from app.utils.migrations       import migrations, create_database

# Models
from app.models import (
    db,
    Users,
    Configs
)

# Flask
from jinja2 import FileSystemLoader
from flask  import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    abort,
    render_template,
    flash
)

# Redis
from app.utils.security import redis

from app.utils.config   import is_setup

recaptcha = ReCaptcha()

def create_app(config="app.config.Config"):
    app = Flask(__name__)

    # Set Config
    app.config.from_object(config)

    with app.app_context():
        # Create Database(if it doesn't created)
        url = create_database()

        # Set MySQL's charset to utf8mb4 forcely
        app.config["SQLALCHEMY_DATABASE_URI"] = str(url)

        # Set Redis Session 
        app.session_interface = redis.RedisSessionInterface()
        
        # Register Database
        db.init_app(app)

        # Create DB Session & Engine (if db is not defined, create db too.)
        db.create_all()

        # Set ReCaptcha
        if is_setup():
            app.config["RECAPTCHA_SITE_KEY"]   = get_config("recaptcha_site_key")
            app.config["RECAPTCHA_SECRET_KEY"] = get_config("recaptcha_secret_key")

        recaptcha.init_app(app)

        # Initialization
        init_template_globals(app)
        init_request_processors(app)

        # Cache Initialization
        cache.init_app(app)
        app.cache = cache

        from app.admin      import admin
        from app.handler    import page_not_found, forbidden, general_error, gateway_error, too_many_requests
        
        app.register_blueprint(admin)

        # Error Handler
        app.register_error_handler(403, forbidden)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(429, too_many_requests)
        app.register_error_handler(500, general_error)
        app.register_error_handler(502, gateway_error)

        return app
