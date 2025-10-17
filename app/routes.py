# app/routes.py
import os
from flask import Flask
from app.controllers.broswer_login_controller import browser_login, browser_login_post
from app.controllers.health_controller import health_check
from app.controllers.singup_controller import user_singup
from app.controllers.login_controller import user_login
from app.controllers.generate_otp_controller import generate_otp
from app.controllers.validate_otp_controller import validate_otp
from app.controllers.member_transactions_accrual import member_transactions_accural
from app.controllers.sso_member_callback_redirect_register import sso_member_callback_redirect_register
from app.controllers.obtain_tokens_controller import obtain_tokens

BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "HTML"))

def configure_routes(app):
    app.route('/', methods=['GET'])(obtain_tokens)
    app.route('/health', methods=['GET'])(health_check)
    app.route('/login', methods=['GET'])(browser_login)
    app.route('/login', methods=['POST'])(browser_login_post)
    app.route('/v2/user/signup', methods=['POST'])(user_singup)
    app.route('/v1/security/login', methods=['POST'])(user_login)
    app.route('/v1/security/generate-otp', methods=['POST'])(generate_otp)
    app.route('/v1/security/validate-otp', methods=['POST'])(validate_otp)
    app.route('/v1/member-transactions/points/accrual/delivery', methods=['POST'])(member_transactions_accural)
    app.route('/sso/v2/member/callback/register', methods=['POST'])(sso_member_callback_redirect_register)
    
configure_routes(app)
