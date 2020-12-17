from flask  import current_app as app
from flask  import (
    flash,
    request,
    redirect,
    url_for,
    render_template
)

from app.models             import db, Hosts

from app.utils.decorators   import authed_only
from app.utils.wol          import wakeup

# Get Blueprint
from app.admin import admin

@admin.route("/admin/hosts", methods=['GET', 'POST'])
@authed_only
def hosts():
    hosts   = db.session.query( Hosts.idx,
                                Hosts.name,
                                Hosts.mac,
                                Hosts.ip,
                                Hosts.broadcast).all()

    return render_template( f"/admin/hosts/index.html",
                            hosts=hosts )


@admin.route("/admin/hosts/<host_idx>", methods=['GET', 'POST'])
@authed_only
def host_detail(host_idx):
    # Get host object
    host    = Hosts.query.filter_by(idx=host_idx).one_or_none()

    return render_template( f"/admin/hosts/detail.html",
                            host=host )


@admin.route("/admin/hosts/add", methods=['POST'])
@authed_only
def host_add():
    name        = request.form.get("name",      type=str) 
    mac         = request.form.get("mac",       type=str)
    ip          = request.form.get("ip",        type=str)
    broadcast   = request.form.get("broadcast", type=int) # if not None == True

    host        = Hosts(name=name,
                        mac=mac,
                        ip=ip,
                        broadcast=broadcast)
    
    try:
        db.session.add(host)
    except Exception as e:
        db.session.rollback()
        flash(message="Failed to add your host.", category="error")
        return redirect(url_for(".host_add"))
    else:
        db.session.commit()

    flash(message="Host added successfully.", category="success")
    return redirect(url_for(".hosts"))


@admin.route("/admin/hosts/edit/<int:host_idx>", methods=['POST'])
@authed_only
def host_edit(host_idx):
    name            = request.form.get("name",      type=str) 
    mac             = request.form.get("mac",       type=str)
    ip              = request.form.get("ip",        type=str)
    broadcast       = request.form.get("broadcast", type=int) # if not None == True

    # Get host object
    host            = Hosts.query.filter_by(idx=host_idx).one_or_none()

    host.name       = name
    host.mac        = mac
    host.ip         = ip
    host.broadcast  = broadcast

    # Commit into database
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(message="Failed to edit your host.", category="error")
        return redirect(url_for(".host_edit"))
    else:
        db.session.commit()

    flash(message="Host edited successfully.", category="success")
    return redirect(url_for(".hosts"))


@admin.route("/admin/hosts/del/<int:host_idx>", methods=['POST'])
@authed_only
def host_del(host_idx):
    name    = request.form.get("name",  type=str)

    # Get host object
    host    = Hosts.query.filter_by(idx=host_idx).one_or_none()

    if name != host.name:
        flash(message="Host name is not matched.", category="error")
        return redirect(url_for(".host_detail"))

    # Commit into database
    try:
        db.session.delete(host)
    except Exception as e:
        db.session.rollback()
        flash(message="Failed to delete your host.", category="error")
        return redirect(url_for(".host_detail"))
    else:
        db.session.commit()

    flash(message="Host deleted successfully.", category="success")
    return redirect(url_for(".hosts"))


@admin.route("/admin/hosts/up/<int:host_idx>", methods=['GET'])
@authed_only
def host_up(host_idx):
    host_name = wakeup(host_idx)
    return f"Send magic packet to `{host_name}``."