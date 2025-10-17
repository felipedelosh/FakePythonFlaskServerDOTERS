# app/controllers/obtain_tokens_controller.py
from flask import request
from flask import render_template
from app.helpers.response import success_response
from app.helpers.response import error_response

def obtain_tokens():
    try:
        params = request.args.to_dict(flat=True)

        print(params)
        return render_template("login.html")
    except:
        return render_template("login.html")
