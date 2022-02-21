#requirements to signout
from flask import Blueprint, jsonify, request
from database_controler import mysql
from helpers.tokens import decrypt_token
from helpers.verify_token import token_required

signout_route = Blueprint('signout_route', __name__)

'''
here user is signed out, and status of user is false, which means
the user is not logged in on this application
'''

@signout_route.route('/signout', methods=['GET'])
@token_required
def signout_user():
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call signout_user(%s)',
                               (user_data.get('id')))
        connection.commit()
        response = jsonify({
            "message":"thank you for your preferences, come back soon!"
        })
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code=500
        return response
