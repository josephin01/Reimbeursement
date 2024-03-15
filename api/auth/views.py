from flask import Blueprint, request, g
from api.auth.services import get_user_data, check_user_password, token_gen_for_user
from common.response import success_response, failure_response


auth_api = Blueprint('auth_api', __name__, url_prefix='/auth')


@auth_api.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)
    if email and password:
        g.curUser = get_user_data(email)
        if g.get('curUser') is not None:
            if check_user_password(password):
                user = g.get('curUser')
                token = token_gen_for_user(email=user.email)
                user_data = {
                    'role': user.role.value,
                    'empId': user.empId,
                    'fname': user.fname,
                    'lname': user.lname,
                    'profile': user.profile,
                    'token': token
                }
                return success_response(status_code=200, content=user_data)
            return failure_response(status_code=401, content="Password incorrect")
        return failure_response(status_code=404, content='User not found')
    return failure_response(status_code=400, content="Bad request")
