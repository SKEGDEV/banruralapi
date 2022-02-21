#Requeriments to validation of tokens
from flask import jsonify, request
from functools import wraps
from database_controler import mysql
from helpers.tokens import decrypt_token

'''
here is verify of token, and this evaluate if token is on header,
and verify if token is of a user stored on database, this is efective in this test system
'''
def verify_token():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer ' not in auth_header:
            return {"message":"sorry this user dont have a token session"}
        split = auth_header.split(' ')
        if not len(split) == 2:
            return {"message":"sorry this user dont have a token session"}
        decode_data = decrypt_token(split[1])
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_user_to_validation(%s)',
                               (decode_data.get('id')))
        user = database_query.fetchall()
        connection.commit()
        user_status = False
        for data in user:
            user_status = data[3]
        if not user:
            return {"message":"sorry this token is incorrect"}
        if user_status == False:
            return {"message": "sorry this user is not logged in"}
        else:
            return {"user":decode_data}
    except Exception as e:
        return {"message":"sorry this token is invalid"}

'''here is to verify token required, if verify_token is correct, this function
checks if user can continue or not'''
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        res = verify_token()
        if not res.get('user'):
            response = jsonify({
                "message":res.get('message')
            })
            response.status_code=500
            return response
        else:
            return f( *args, **kwargs)
    return decorated




