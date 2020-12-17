import hashlib

from flask  import current_app as app
from flask  import (
    flash,
    request,
    redirect,
    url_for,
    render_template,
    send_file
)

from app.utils      import set_config

from app.models     import db, Users

from app.utils.config        import is_setup

# Get Blueprint
from app.admin import admin

@admin.route("/admin/setup", methods=['GET', 'POST'])
def setup():
    if not is_setup():
        if request.method == "POST":
            # Admin Account
            uid         = request.form.get("uid")
            email       = request.form.get("email")
            password    = request.form.get("password")

            account     = Users(uid=uid,
                                email=email,
                                password=hashlib.sha3_512(password.encode()).hexdigest())

            # Commit admin account
            try:
                db.session.add(account)
            except Exception as e:
                flash(message=f"Admin  : {e._message}", category="error")
                db.session.rollback()
                return redirect(url_for("admin.setup"))

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

            # Setup completed
            set_config("setup", True)

            return redirect(url_for("admin.index"))
        
        # if setup is not completed
        return render_template( f"/admin/configs/setup.html" )

    else:
        flash(message="Your flask had been set already.", category="info")
        return redirect(url_for("admin"))
        