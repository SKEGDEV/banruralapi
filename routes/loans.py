from flask import Blueprint, request, jsonify
from database_controler import mysql
from helpers.tokens import decrypt_token, generate_expire_days
from helpers.verify_token import token_required
from datetime import datetime

loan_routes= Blueprint('loan_routes', __name__)

@loan_routes.route('/add-loan', methods=['POST'])
@token_required
def add_loan():
    token = request.headers['Authorization'].split(' ')[1]
    user_data = decrypt_token(token)
    set_data = request.get_json()
    payment_date = generate_expire_days(31)
    loan_cuote = float(set_data["loan_balance"])/24
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call add_user_loan(%s, %s, %s, %s, %s)',
                               (
                                   user_data.get('id'),
                                   set_data["account_id"],
                                   set_data["loan_balance"],
                                   loan_cuote,
                                   payment_date
                               ))
        connection.commit()
        response = jsonify({
            "message":"loan added succesful"
        })
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code = 500
        return response

@loan_routes.route('/get-loan-information', methods=["GET"])
@token_required
def get_loan_information():
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_loan_information(%s)',
                               (user_data.get('id')))
        loan_information = database_query.fetchall()
        connection.commit()
        if(len(loan_information)>0):
            response = jsonify({
                "message":"this is data of loans",
                "data":loan_information
            })
            response.status_code=200
            return response
        else:
            response = jsonify({
                "message":"sorry you dont have a bank loan"
            })
            response.status_code = 200
            return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code = 500
        return response

@loan_routes.route('/make-payment', methods=['POST'])
@token_required
def make_payment():
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    next_payment_day = generate_expire_days(31)
    payment_date = datetime.now().strftime("%Y-%m-%d")
    set_data = request.get_json()
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call make_payment(%s, %s, %s, %s, %s)',
                               (user_data.get('id'),
                                set_data["type_payment"],
                                payment_date,
                                next_payment_day,
                                set_data["id_loan"]
                                ))
        connection.commit()
        response = jsonify({
            "message":"your payment is successful"
        })
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code = 500
        return response

@loan_routes.route('/get-payments', methods=['GET'])
@token_required
def get_payments():
    token = request.headers['Authorization'].split(" ")[1]
    user_data = decrypt_token(token)
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_payment_register(%s)',
                               (user_data.get('id')))
        payments_information = database_query.fetchall()
        connection.commit()
        if(len(payments_information)>0):
            response = jsonify({
                "message":"this is information of your payments",
                "data":payments_information
            })
            response.status_code =200
            return response
        else:
            response = jsonify({
                "message":"sorry you dont make a payment loan"
            })
            response.status_code =200
            return response
    except Exception as e:
        response = jsonify({
            "message": "sorry an error ocurred",
            "error":str(e)
        })
        response.status_code=500
        return response
