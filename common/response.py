from common.strings import Status
from flask import jsonify


def success_response(status_code=200, content='success'):
    response = {
        'status': Status.success,
        'content': content,
        'status_code': status_code
    }
    return jsonify(response), status_code


def failure_response(status_code=500, content='Internal Server Error'):
    response = {
        'status': Status.failed,
        'content': content,
        'status_code': status_code
    }
    return jsonify(response), status_code
