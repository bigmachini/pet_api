from functools import wraps
from flask import request, jsonify
import datetime

from app.models import App, Access


def app_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app_id = request.headers.get('X-APP-ID')
        app_token = request.headers.get('X-APP-TOKEN')

        #Check if app_id or app_token exist
        if app_id is None or app_token is None:
            return jsonify({}), 403
        
        #check is app exists in database
        app = App.objects.filter(app_id=app_id).first()
        if not app:
            return jsonify({}), 403

        #check app access from database
        access = Access.objects.filter(app=app).first()

        #No access for app
        if not access:
            return jsonify({}), 403

        #token invalid from issued
        if access.token != app_token:
            return jsonify({}), 403
            
        #token expired
        if access.expires < datetime.datetime.now():
            error = {
                'code': 'TOKEN_EXPIRED'
            }
            return jsonify({'error': error}), 403

        return f(*args, **kwargs)
    return decorated_function
