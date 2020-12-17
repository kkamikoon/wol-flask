from flask import (
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from datetime import datetime

from werkzeug.urls  import (
    url_parse
)

from app.utils.user import (
    authed
)

from app.utils.url     import (
    current_url,
    current_endpoint
)

from app.utils.config  import is_setup
from app.utils         import get_config

from app.models        import db

def init_template_globals(app):
    app.jinja_env.globals.update(get_config=get_config)
    app.jinja_env.globals.update(authed=authed)
    app.jinja_env.globals.update(is_setup=is_setup)
    app.jinja_env.globals.update(current_url=current_url)
    app.jinja_env.globals.update(current_endpoint=current_endpoint)

    @app.template_filter("endpoint_for_header")
    def endpoint_for_header(endpoint):
        '''
        :param endpoint:  string value of endpoint like 'admin.dashboard'
        '''
        return endpoint.split('.')[-1].capitalize()


def init_request_processors(app):
    # @app.before_request
    # def needs_setup():
    #     if is_setup() is False:
    #         if request.endpoint in (
    #             "admin.setup",
    #             "admin.themes"
    #         ):
    #             return
    #         else:
    #             return redirect(url_for("admin.setup"))

    @app.before_request
    def domain_check():
        if get_config('domain_check'):
            if url_parse(request.host_url).host != get_config('wol_domain'):
                return ""