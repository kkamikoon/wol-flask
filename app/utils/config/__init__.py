from flask          import current_app as app
from flask.helpers  import safe_join

from app.utils      import set_config, get_config


def is_setup():
    return bool(get_config("setup")) is True
