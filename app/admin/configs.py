from flask   import current_app as app
from flask   import (
    flash,
    request,
    redirect,
    url_for,
    render_template
)

from app.utils.decorators import authed_only

# Get Blueprint
from app.admin import admin


@admin.route("/admin/configs", methods=['GET', 'POST'])
# @authed_only
def configs():
    if request.method == "POST":        
        flash(message="[Example]Configs are changed successfully.", category="success")
        # return redirect(url_for("admin.index"))
        return redirect(url_for("admin.hosts"))

    return render_template( f"/admin/configs/configs.html" )