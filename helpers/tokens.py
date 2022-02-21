#this is for use jwt to user validation, and when is a new user 
from jwt import encode, decode
from os import getenv
from datetime import datetime, timedelta

def generate_expire_days(days):
    date_now = datetime.now()
    return  (date_now + timedelta(days=days)).strftime("%Y-%m-%d")

def generate_token(data: dict):
    return encode(payload={**data, "expiration":str(generate_expire_days(2))},
                  key=getenv("secret_key"),
                  algorithm="HS256")

def decrypt_token(token):
    return decode(token, key=getenv("secret_key"), algorithms="HS256")
