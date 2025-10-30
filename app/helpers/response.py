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

def unauthorized():
    return jsonify({
        "error": {
            "message": "Unauthorized",
            "code": "UNAUTHORIZED"
        },
        "type": "UNAUTHORIZED",
        "action": "STOP"
    }), 401

def forbidden(msg="Forbidden"):
    return error_response(msg, "FORBIDDEN", 403)

def server_error(msg="Internal Server Error"):
    return error_response(msg, "INTERNAL_SERVER_ERROR", 500)

def singup_error_duplicated(customerNumber, firstName, lastName):
    return jsonify({
        "message": "Error has occurred",
        "type": "INVALID",
        "action": "CANCEL",
        "parameters": [
            {
                "key": customerNumber,
                "message": f"{firstName} {lastName}"
            }
        ]
    }), 400

def singup_error_general(key, message, http_code=500):
    return jsonify({
        "type": "INVALID_PARAMETER",
        "action": "CANCEL",
        "message": "Validation error has occurred",
        "diagnosticInformation": None,
        "exceptionId": None,
        "parameters": [
            {
                "key": key,
                "message": message
            }
        ],
        "code": "GENERIC_VALIDATION_ERROR"
    }), http_code
