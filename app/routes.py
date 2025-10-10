# app/routes.py
from flask import Flask
from app.controllers.health_controller import health_check
from app.controllers.singup_controller import user_singup
from app.controllers.login_controller import user_login
from app.controllers.generate_otp_controller import generate_otp
from app.controllers.validate_otp_controller import validate_otp

app = Flask(__name__)

def configure_routes(app):
    app.route('/health', methods=['GET'])(health_check)
    app.route('/v2/user/signup', methods=['POST'])(user_singup)
    app.route('/v1/security/login', methods=['POST'])(user_login)
    app.route('/v1/security/generate-otp', methods=['POST'])(generate_otp)
    app.route('/v1/security/validate-otp', methods=['POST'])(validate_otp)
    
configure_routes(app)
