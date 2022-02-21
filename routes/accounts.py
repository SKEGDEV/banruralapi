from flask import Blueprint, request, jsonify
from database_controler import mysql
from helpers.tokens import decrypt_token
from helpers.verify_token import token_required
import random

accounts_routes = Blueprint('accounts_routes', __name__)

@accounts_routes.route('/add-account', methods=['POST'])
@token_required
def add_user_account():
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    try:
        account_number = random.randint(10000000, 99999999)
        set_data = request.get_json()
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call add_bank_account(%s, %s, %s, %s, %s)',
                               (
                                   account_number,
                                   user_data.get('id'),
                                   2000,
                                   10000,
                                   set_data['account_type']
                               ))
        connection.commit()
        response = jsonify({
            "message":"your account is created succesfull"
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

@accounts_routes.route('/get-accounts', methods=['GET'])
@token_required
def get_information_accounts():
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_account_information(%s)',
                               (user_data.get('id')))
        account_data = database_query.fetchall()
        connection.commit()
        if(len(account_data) > 0):
            response = jsonify({
                "message":"this is data of your accounts",
                "data":account_data
            })
            response.status_code=200
            return response
        else:
            response = jsonify({
                "message":"sorry you dont have a bank account"
            })
            response.status_code =200
            return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code = 500
        return response

