from flask import current_app as app
from flask import request

def current_url():
    return request.url_rule.rule

def current_endpoint():
    return request.endpoint