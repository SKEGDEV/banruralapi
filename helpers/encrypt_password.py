from flask_bcrypt import check_password_hash, generate_password_hash

def encrypt_password(password_entry):
    return generate_password_hash(password_entry.encode(), 10)

def match_password(database_password, password_entry):
    return check_password_hash(database_password.encode(), password_entry.encode())

