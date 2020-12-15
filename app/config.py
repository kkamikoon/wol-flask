import os

class Config(object):
    """
    Configuration of Python Flask
    """
    # Session(Redis) Settings
    SESSION_COOKIE_NAME = "WAKE-ON-LAN-SESSION"
    SESSION_TYPE        = "redis"

    # Cache Type
    CACHE_TYPE          = "filesystem"
    CACHE_DIR           = os.path.join(
        os.path.dirname(__file__), os.pardir, ".cache", "filesystem_cache"
    )
    CACHE_THRESHOLD = (
        0
    )

    # SQLAlchemy Settings
    db_info         = {
        "user"      : "wol",
        "password"  : "wol",
        "host"      : "localhost",
        "port"      : 3306,
        "database"  : "wol"
    }
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}?charset=utf8"
    #SQLALCHEMY_DATABASE_URI = f"sqlite3://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    TRUSTED_PROXIES     = [
        r"^127\.0\.0\.1$",
        # Remove the following proxies if you do not trust the local network
        # For example if you are running a CTF on your laptop and the teams are
        # all on the same network
        r"^::1$",
        r"^fc00:",
        r"^10\.",
        r"^172\.(1[6-9]|2[0-9]|3[0-1])\.",
        r"^192\.168\.",
    ]

    # Flask-ReCaptcha Configs - ReCaptcha V2(Flask ReCaptcha doesn't support ReCaptcha V3)
    RECAPTCHA_ENABLED   = True
    RECAPTCHA_SITE_KEY  = "[YOUR-SITE-KEY]"
    RECAPTCHA_SECRET_KEY= "[YOUR-SECRET-KEY]"
    RECAPTCHA_THEME     = "dark"