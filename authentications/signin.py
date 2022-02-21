from flask import Blueprint, request, jsonify
from helpers.encrypt_password import match_password
from database_controler import mysql
from helpers.tokens import generate_token
from helpers.database_querys import signin_user


signin_route = Blueprint('signin_route',__name__)

@signin_route.route('/signin', methods=['POST'])
def validate_user():
    try:
        set_data = request.get_json()
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_user_informacion_to_login(%s)',
                               (set_data["nit"]))
        user_data = database_query.fetchall()
        connection.commit()
        if(len(user_data)>0):
            user_information = None
            database_password=""
            for user in user_data:
                user_information = {
                    "id":user[0],
                    "name":user[1]
                }
                database_password = user[3]
            if(match_password(database_password, set_data["password"])):
                signin_user(user_information.get("id"))
                token = generate_token(user_information)
                response = jsonify({
                    "token":token.decode(),
                    "name":user_information["name"],
                    "message":"this user is correct"
                })
                response.status_code = 200
                return response
            else:
                response = jsonify({
                    "message":"sorry your password is incorrect",
                })
                response.status_code = 200
                return response
        else:
            response = jsonify({
                "message":"sorry this user dont exist in this database"
            })
            response.status_code = 200
            return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        print(str(e))
        response.status_code = 500
        return response


