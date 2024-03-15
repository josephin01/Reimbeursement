import bcrypt as en


def encrypt_password(password):
    hash_password = en.hashpw(password=password.encode('utf8'), salt=en.gensalt())
    return hash_password.decode('utf8')


def check_password(password, hash_password):
    return en.checkpw(password=password, hashed_password=hash_password)
