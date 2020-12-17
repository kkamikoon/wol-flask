from flask   import current_app as app
from flask   import render_template

# Get Blueprint
from app.admin import admin

@admin.route("/admin/403", methods=['GET'])
def handler_forbidden():
    return render_template(f"/admin/handler/403.html"), 403


@admin.route("/admin/404", methods=['GET'])
def handler_page_not_found():
    return render_template(f"/admin/handler/404.html"), 404


@admin.route("/admin/429", methods=['GET'])
def handler_too_many_requests():
    return render_template(f"/admin/handler/429.html"), 429


@admin.route("/admin/500", methods=['GET'])
def handler_general_error():
    return render_template(f"/admin/handler/500.html"), 500


@admin.route("/admin/502", methods=['GET'])
def handler_gateway_error():
    return render_template(f"/admin/handler/502.html"), 502

