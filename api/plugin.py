from api.identity import Identity
from functools import wraps
from flask import request, current_app


def need_auth(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        headers = dict(request.headers)
        identity = Identity.get(headers, current_app.config)
        if identity is None:
            return "Restricted access", 401
        kwargs["identity"] = identity
        return f(*args, **kwargs)

    return wrap
