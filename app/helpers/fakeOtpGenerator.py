# app/helpers/fakeOtpGenerator.py
import random

def generate_otp_code() -> str:
    return f"{random.randint(100001, 999999)}"
