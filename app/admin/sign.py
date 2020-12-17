import hashlib

from flask  import current_app as app
from flask  import (
    request,
    redirect,
    url_for,
    render_template,
    flash,
)
from ..     import recaptcha

from app.utils.security.auth import (
    signin_user,
    signout_user,
)

from app.utils.decorators import ratelimit, authed_only

from app.utils      import user, get_config

from app.models     import db, Users
from app.utils.user import authed

from app.admin      import admin

@admin.route("/sign", methods=['GET'])
def sign():
    # if authed():
    #     flash(message=f"Already Signed In", category="warning")
    #     return redirect(url_for(".index"))
    return render_template(f"/admin/main/sign.html")


@admin.route("/sign/in", methods=['POST'])
# @ratelimit(method="POST", limit=5, interval=300)
def signin():
    # ------------------------------------------------------------
    # Recaptcha V2 Verifying
    # if not recaptcha.verify():
    #     flash(message="Please verifying reCaptcha.", category="error")
    #     return redirect(url_for(".sign"))

    # ------------------------------------------------------------
    # REQUEST POST
    uid         = request.form.get("uid",       type=str)
    password    = request.form.get("password",  type=str)
    # password    = hashlib.sha3_512(request.form.get("password", type=str).encode()).hexdigest()
    
    # user_info   = db.session.query( Users.idx,
    #                                 Users.uid,
    #                                 Users.email ).\
    #                 filter( Users.uid       == uid,
    #                         Users.password  == password).one_or_none()

    # if user_info == None:
    if uid != "kkamikoon" or password != "kkamikoon":
        flash(message="[Example]Failed to sign in. {uid : 'kkamikoon', 'password' : 'kkamikoon''}", category="error")
        return redirect(url_for(".sign"))
    else:
        flash(message="[Example]Sign In successfully.", category="success")
        # signin_user(user_info)
        return redirect(url_for(".hosts"))


@admin.route("/sign/out", methods=['GET'])
@authed_only
def signout():
    # ------------------------------------------------------------
    # if user.authed():
    #     # Delete from Redis
    #     sid = request.cookies.get(app.session_cookie_name)
    #     app.session_interface.store.delete(sid)
        
    #     # Delete from Client
    #     signout_user()
    
    return redirect(url_for(".index"))
    