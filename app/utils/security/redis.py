# Redis  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import  redis
import  _pickle as cPickle
from    flask                   import session
from    flask.sessions          import SessionInterface, SessionMixin
from    werkzeug.datastructures import CallbackDict
from    uuid                    import uuid4
from    datetime                import datetime, timedelta
from    base64                  import b64encode
from    hashlib                 import sha3_512
from    os                      import urandom
from    string                  import ascii_lowercase, ascii_uppercase, digits


class RedisSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid        = sid
        self.modified   = False

class RedisSessionInterface(SessionInterface):
    def __init__(self, host='localhost', port=6379, db=0, timeout=3600):
        self.store      = redis.StrictRedis(host=host,
                                            port=port,
                                            db=db)
        self.timeout    = timeout

    def open_session(self, app, request):
        sid, stored_session = self.get_session(app, request)

        if stored_session:
            # Check if the session isn't expired
            if stored_session.get('expiration') > datetime.utcnow ():
                return RedisSession(initial=stored_session['data'],
                                        sid=stored_session['sid'])

        # If there was no session or it was expired...
        # Generate a random id and create an empty session
        sid = self.sid_with_salt(128)
        return RedisSession(sid=sid)


    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        # We're requested to delete the session
        if not session:
            response.delete_cookie( app.session_cookie_name,
                                    domain=domain)
            return

        # Refresh the session expiration time
        # First, use get_expiration_time from SessionInterface
        # If it fails, add 1 hour to current time
        if self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() + timedelta(hours=1)

        # Update the Redis document, where sid equals to session.sid
        ssd = {
            'sid'       : session.sid,
            'data'      : session,
            'expiration': expiration,
            'idx'       : session.get("idx")
        }
        ssstr = cPickle.dumps(ssd)
        self.store.setex(session.sid, self.timeout, ssstr)
        # Refresh the cookie
        response.set_cookie(app.session_cookie_name,
                            session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True,      # Browser
                            secure=False,       # SSL Option -- Real Server : True
                            domain=domain)


    def sid_with_salt(self, salt_byte=64):
        sid = b64encode((str(uuid4()) + "-" + sha3_512(urandom(salt_byte)).hexdigest()).encode())
        return sid

    
    def get_session(self, app, request):
        # Get session id from the cookie
        sid = request.cookies.get(app.session_cookie_name)
        
        # If id is given (session was created)
        if sid:
            # Try to load a session from Redisdb
            stored_session  = None
            ssstr           = self.store.get(sid)

            if ssstr:
                stored_session = cPickle.loads(ssstr)
        else:
            return None, None

        return sid, stored_session


    def duplication(self, user):
        for key in self.store.keys():
            stored_session = cPickle.loads(self.store.get(key.decode()))

            if user is not None:
                if stored_session['idx'] == user.idx:
                    # If the session duplicated. Delete session.
                    self.store.delete(key.decode())
                    return
        
        