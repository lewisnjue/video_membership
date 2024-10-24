from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def generate_hash(pw_raw):
    ph = PasswordHasher()
    return ph.hash(pw_raw)

def verify_hash(pw_hash,pw_raw):
    ph = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = ph.verify(pw_hash,pw_raw)
    except VerifyMismatchError as e:
            verified = False
            msg = "invalid password"
            return verified,msg
    except :
        verified = False
        msg = "something went wrong"
    return verified,msg

