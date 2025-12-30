# utils.py

import os
import json
from datetime import datetime, timedelta

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        elif isinstance(obj, set):
            return list(obj)
        else:
            return super().default(obj)

def read_env_variable(var_name, default=None):
    value = os.environ.get(var_name)
    return value if value else default

def generate_token(user_id, expires_in=timedelta(hours=1)):
    expires_at = datetime.utcnow() + expires_in
    token = f"auth-gateway:{user_id}:{expires_at.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    return token

def validate_token(token):
    try:
        user_id, expires_at = token.split(":", 2)
        expires_at = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%SZ')
        if datetime.utcnow() <= expires_at:
            return user_id
    except ValueError:
        pass
    return None