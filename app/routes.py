# app/routes.py
from flask import Flask
from app.controllers.health_controller import health_check
from app.controllers.singup_controller import user_singup
from app.controllers.login_controller import user_login

app = Flask(__name__)

def configure_routes(app):
    app.route('/health', methods=['GET'])(health_check)
    app.route('/v2/user/signup', methods=['POST'])(user_singup)
    app.route('/v1/security/login', methods=['POST'])(user_login)
    
configure_routes(app)
