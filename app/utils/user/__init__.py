from flask import current_app as app
from flask import request, session

from app.models import Users, db

import re

def authed():
    return bool(session.get("idx", False))


def get_ip(req=None):
    if req is None:
        req = request
    
    trusted_proxies = app.config["TRUSTED_PROXIES"]
    combined        = "(" + ")|(".join(trusted_proxies) + ")"
    route           = req.access_route + [req.remote_addr]

    for addr in reversed(route):
        if not re.match(combined, addr):  # IP is not trusted but we trust the proxies
            remote_addr = addr
            break
        else:
            remote_addr = req.remote_addr
            
    return remote_addr


def get_ip_x_forwarded_for(req=None):
    if req is None:
        req = request
    
    remote_addr = req.headers.get('X-Forwarded-For')

    if remote_addr == None:
        return request.remote_addr
    
    return remote_addr