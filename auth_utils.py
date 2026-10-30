from functools import wraps
from flask_jwt_extended import verify_jwt_in_request


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()   # returns 401 if missing/invalid/expired
        return fn(*args, **kwargs)
    return wrapper