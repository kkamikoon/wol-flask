import os

from flask  import current_app as app
from flask  import (
    Blueprint,
    request,
    redirect,
    url_for,
    send_file,
    abort,
    flash,
    render_template
)

from flask.helpers          import safe_join

from datetime               import datetime

from app.utils              import get_config
from app.utils.user         import authed
from app.utils.decorators   import authed_only

from app.models             import db

admin = Blueprint("admin", __name__)

from app.admin              import setup
from app.admin              import configs
from app.admin              import sign
from app.admin              import hosts

@admin.route("/", methods=['GET'])
@admin.route("/admin", methods=['GET'])
def index():
    if authed():
        return redirect(url_for(".hosts"))
    
    return redirect(url_for(".sign"))


@admin.route("/statics/<path:path>")
def themes(path):
    filename = safe_join(app.root_path, "static", "admin", path)

    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)
