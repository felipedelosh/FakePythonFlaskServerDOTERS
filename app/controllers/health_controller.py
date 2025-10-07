from flask import jsonify
from app.helpers.response import create_response

def health_check():
    return create_response(True, "Server RUN", 200)
