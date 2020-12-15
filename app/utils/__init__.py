from flask import current_app as app

from app.models import Configs, db

import six

if six.PY2:
    string_types = (str, unicode)  # noqa: F821
    text_type = unicode  # noqa: F821
    binary_type = str
else:
    string_types = (str,)
    text_type = str
    binary_type = bytes


# @cache.memoize()
def _get_config(key):
    config = Configs.query.filter_by(key=key).first()

    if config and config.value:
        value = config.value
        
        if value and value.isdigit():
            return int(value)
        elif value and isinstance(value, six.string_types):
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
            else:
                return value
    
    return KeyError


def get_config(key, default=None):
    value = _get_config(key)
    if value is KeyError:
        return default
    else:
        return value


def set_config(key, value):
    config = Configs.query.filter_by(key=key).first()
    if config:
        config.value = value
    else:
        config = Configs(key=key, value=value)
        db.session.add(config)
    db.session.commit()
    
    return config

