from passlib.hash import pbkdf2_sha256


def hash_password(password):
    return pbkdf2_sha256.using(rounds=100000, salt_size=32).hash(password)


def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)
