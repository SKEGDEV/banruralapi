from flask import Blueprint, request, jsonify
from database_controler import mysql
from helpers.tokens import decrypt_token
from helpers.verify_token import token_required
import random

card_routes = Blueprint('card_routes', __name__)

@card_routes.route('/add-card', methods=['POST'])
@token_required
def add_card():
    card_number = random.randint(100000000, 9999999999)
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    set_data = request.get_json()
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call add_bank_card(%s, %s, %s, %s)',
                               (
                                   user_data.get('id'),
                                   card_number,
                                   4000,
                                   set_data["card_type"]
                               ))
        connection.commit()
        response = jsonify({
            "message":"this card is added successful"
        })
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({
            "message": "sorry an error ocurred",
            "error":str(e)
        })
        response.status_code = 500
        return response

@card_routes.route('/get-cards-information', methods=["GET"])
@token_required
def get_cards():
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_card_information(%s)',
                               (user_data.get('id')))
        card_information = database_query.fetchall()
        connection.commit()
        if(len(card_information)>0):
            response = jsonify({
            "message":"welcome this is your card information",
            "data":card_information
            })
            response.status_code=200
            return response
        else:
            response = jsonify({
                "message":"sorry you dont have a bank card"
            })
            response.status_code =200
            return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code=500
        return response



