from flask import jsonify
from app.helpers.response import success_response

def health_check():
    return success_response("Server RUN", 200)
