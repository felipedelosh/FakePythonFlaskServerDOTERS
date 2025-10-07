# app/helpers/response.py
from flask import jsonify

def success_response(data, http_code=200):
    return jsonify({
        "data": data,
        "type": "SUCCESS",
        "action": "CONTINUE"
    }), http_code

def error_response(message="Bad Request Exception", code="BAD_REQUEST", http_code=400):
    return jsonify({
        "error": {
            "message": message,
            "code": code
        },
        "type": "ERROR",
        "action": "CANCEL"
    }), http_code

def unauthorized(msg="Unauthorized"):
    return error_response(msg, "UNAUTHORIZED", 401)

def forbidden(msg="Forbidden"):
    return error_response(msg, "FORBIDDEN", 403)

def server_error(msg="Internal Server Error"):
    return error_response(msg, "INTERNAL_SERVER_ERROR", 500)
