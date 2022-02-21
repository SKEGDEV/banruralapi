from database_controler import mysql

def get_user_data(nit):
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_user_informacion_to_login(%s)', (nit))
        get_user = database_query.fetchall()
        connection.commit()
        if(len(get_user)>0):
            return get_user
        else:
            return None
    except:
        return None

def signin_user(id):
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call signin_user(%s)', (id))
        connection.commit()
    except Exception as e:
        print("an error ocurred error: ", str(e))

def get_id_account(account_number):
    account_id = 0
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_account_id(%s)',
                               (account_number))
        account_information = database_query.fetchall()
        connection.commit()
        for data in account_information:
            account_id = data[0]
        return account_id
    except Exception as e:
        print("an error ocurred error: ", str(e))

