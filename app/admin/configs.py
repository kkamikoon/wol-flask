from hashlib import sha3_512
from flask   import current_app as app
from flask   import (
    flash,
    request,
    redirect,
    url_for,
    render_template,
    session
)

from app.utils      import user, get_config, set_config

from app.models     import db, Configs, Users

from app.utils.decorators import authed_only


# Get Blueprint
from app.admin import admin


@admin.route("/admin/configs", methods=['GET', 'POST'])
@authed_only
def configs():
    if request.method == "POST":
        # Admin Account
        user_idx    = request.form.get("idx",       type=int)
        email       = request.form.get("email",     type=str)
        password    = request.form.get("password",  type=str)

        # Get Admin Account Information
        user_admin  = Users.query.filter_by(idx=user_idx).one_or_none()

        if password != "":
            user_admin.password = sha3_512(password.encode()).hexdigest()

        user_admin.email = email

        # Commit into database
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(message="Failed to edit config.", category="error")
            return redirect(url_for(".configs", user_idx=user_idx))
        else:
            db.session.commit()
        
        # Domain Check
        wol_domain  = request.form.get("wol_domain")
        domain_check= request.form.get("domain_check")

        set_config('wol_domain',    wol_domain)
        set_config('domain_check',  domain_check)

        # Page Settings
        title_tag   = request.form.get("title_tag")
        main_title  = request.form.get("main_title")

        set_config('title_tag',  title_tag)
        set_config('main_title', main_title)

        # reCaptcha Settings
        recaptcha_site_key  = request.form.get("recaptcha_site_key")
        recaptcha_secret_key= request.form.get("recaptcha_secret_key")
        recaptcha_status    = request.form.get("recaptcha_status")

        set_config('recaptcha_site_key',    recaptcha_site_key)
        set_config('recaptcha_secret_key',  recaptcha_secret_key)
        set_config('recaptcha_status',      recaptcha_status)
        
        flash(message="Configs are changed successfully.", category="success")
        return redirect(url_for("admin.index"))

    user        = Users.query.filter_by(idx=session.get("idx")).one_or_none()
    configs     = db.session.query( Configs.key, Configs.value ).all()

    return render_template(f"/admin/configs/configs.html",
                            configs=configs,
                            user=user)
                            