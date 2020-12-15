from flask      import session
from flask      import current_app as app

from app.utils  import user as current_user

from urllib.parse import unquote

def signin_user(user):
    # check duplication
    app.session_interface.duplication(user)

    session["idx"]      = user.idx

def signout_user():
    # Delete from client
    session.clear()
