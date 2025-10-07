# app/routes.py
from flask import Flask
from app.controllers.health_controller import health_check
from app.controllers.singup_controller import user_singup

app = Flask(__name__)

def configure_routes(app):
    app.route('/health', methods=['GET'])(health_check)
    app.route('/v2/user/signup', methods=['POST'])(user_singup)
    
configure_routes(app)
