from flask  import current_app as app
from flask  import (
    Blueprint,
    request,
    redirect,
    url_for,
    send_file,
    abort
)

from flask.helpers          import safe_join

from app.utils.user         import authed

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
