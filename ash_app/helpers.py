from functools import wraps
import secrets

from flask import request, jsonify

from ash_app.models import  User
import decimal
from flask import json

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        # if current_user.admin:
            # return our_flask_function(*args,**kwargs)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert Decimal to String
            return str(obj)
        return super(JSONEncoder,self).default(obj)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS