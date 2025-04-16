from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'super_admin':
            return {"message": "Admin access required"}, 403
        return fn(*args, **kwargs)
    return wrapper
