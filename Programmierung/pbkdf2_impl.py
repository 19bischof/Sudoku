from hashlib import pbkdf2_hmac
import os
import base64
from settings import settings as st
def  hash_of_passw(password,salt: bytes = None):
    encoded_passw = password.encode("utf-8")
    if salt == None:
        salt = base64.b64encode(os.urandom(18))
    # print("salt_used:",salt)
    # print("pass_used:",password)
    keysize = st.cryptic['keysize']
    rounds = st.cryptic['rounds']
    method = st.cryptic['method']
    res = pbkdf2_hmac(method, encoded_passw, salt, rounds, keysize).hex()
    return {"hash":res,"salt":salt.hex()}


