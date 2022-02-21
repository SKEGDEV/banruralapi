#initialitations 
from flask import Flask
#database
from database_controler import mysql
#CORS
from flask_cors import CORS
#.env
from os import getenv
#load env
from dotenv import load_dotenv
#Blueprints
from authentications.signup import signup_route
from authentications.signin import signin_route
from authentications.signout import signout_route
from routes.accounts import accounts_routes
from routes.cards import card_routes
from routes.loans import loan_routes
from routes.transactions import transaction_routes



app = Flask(__name__)
#CORS config
CORS(app)
#database credentials
app.config['MYSQL_DATABASE_HOST'] = getenv("host")
app.config['MYSQL_DATABASE_USER'] = getenv("user")
app.config['MYSQL_DATABASE_PASSWORD'] = getenv("password")
app.config['MYSQL_DATABASE_DB'] = getenv("database")
#start connection with database
mysql.init_app(app)

#blueprints initialitations and label route
app.register_blueprint(signup_route)
app.register_blueprint(signin_route)
app.register_blueprint(signout_route)
app.register_blueprint(accounts_routes, url_prefix='/account')
app.register_blueprint(card_routes, url_prefix='/card')
app.register_blueprint(loan_routes, url_prefix='/loan')
app.register_blueprint(transaction_routes, url_prefix='/transaction')

#run server flask on port 4000
if __name__ == '__main__':
    load_dotenv()
    app.run(port=4000, host='192.168.1.8', debug=True)

