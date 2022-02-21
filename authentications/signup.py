from flask import Blueprint, request, jsonify
from helpers.encrypt_password import encrypt_password
from database_controler import mysql
from helpers.tokens import generate_token
from helpers.database_querys import get_user_data


signup_route = Blueprint('signup_route', __name__)

@signup_route.route('/signup', methods=['POST'])
def register_user():
    set_data = request.get_json()
    save_password = encrypt_password(set_data["password"]) 
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call add_user(%s, %s, %s, %s, %s, %s)',
                               (
                                   set_data["first_name"],
                                   set_data["last_name"],
                                   True,
                                   set_data["dpi"],
                                   set_data["nit"],
                                   save_password
                               ))
        connection.commit()
        user_search = get_user_data(set_data["nit"])
        if(user_search != None):
            user_to_token = None
            first_name= ""
            for user in user_search:
                user_to_token = {
                    "id":user[0],
                    "name":user[1]
                }
                first_name = user[1]
            token = generate_token(user_to_token)
            response_with_token = jsonify({
                "token":token.decode(),
                "first_name":first_name,
                "message":"this user is correct"
            })
            response_with_token.status_code = 200
            return response_with_token
        else:
            response_without_token = jsonify({
                "message":"sorry an error ocurred this user dont have token"
            })
            response_without_token.status_code = 200
            return response_without_token
    except Exception as e:
        response_error = jsonify({
            "message":"sorry an error ocurred",
            "error": str(e)
        })
        response_error.status_code=500
        return response_error
