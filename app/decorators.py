from functools import wraps
from flask import request, jsonify
import datetime

from app.models import App,Access


def app_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app_id = request.headers.get('X-APP-ID')
        # app_secret = request.headers.get('X-APP-SECRET')
        # if app_id is None:
        #     return jsonify({}), 403

        # if app_id != 'elisha' or app_secret != "mySecret":
        #     return jsonify({}), 403


        return f(*args, **kwargs)
    return decorated_function


     
 