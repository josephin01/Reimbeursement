from api.auth.controller import get_data
from flask import g
from common.utils.hashing import check_password
from common.utils.token import gen_token


def get_user_data(email):
    return get_data(email)


def check_user_password(password):
    return True if password == g.get('curUser').password else False
    # password = password.encode('utf8')
    # hash_password = g.get('curUser').password.encode('utf8')
    # return check_password(password, hash_password)


def token_gen_for_user(email):
    return gen_token(identity=email)
