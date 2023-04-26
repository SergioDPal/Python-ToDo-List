from config import get_app_config
from flask import abort
from models import User, user_schema


def read_one(user_id):
    user = User.query.get(user_id)

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(
            404, f"User with ID {user_id} not found"
        )


def create(user):
    username = user.get("username")
    password = user.get("password")
    existing_user = User.query.filter_by(username=username).first()
    if existing_user is None:
        new_user = User(username=username, password=password)
        get_app_config().db.session.add(new_user)
        get_app_config().db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(
            409,
            f"User with username {username} already exists"
        )


def check_password_is_correct(user):
    username = user.get("username")
    password = user.get("password")
    existing_user = User.query.filter_by(username=username).first()
    if existing_user is not None:
        if existing_user.password == password:
            return True
        else:
            return False
    else:
        abort(
            404,
            f"User with username {username} not found"
        )
