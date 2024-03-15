from flask_jwt_extended import create_access_token, create_refresh_token


def gen_token(identity):
    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)
    return {'access_token': access_token, 'refresh_token': refresh_token}
