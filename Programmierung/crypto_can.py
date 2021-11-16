import os
from cryptography import fernet

enc_file_name = "welcomeUser.enc"
dec_file_name = "welcomeUser1.db"


#def write_key():
    # """
    # Generates a key and save it into a file
    # """
    # key = fernet.generate_key()
    # with open("key.key", "wb") as key_file:
    #     key_file.write(key)

def read_key():
    with open('key.key', 'rb') as filekey:
        key = filekey.read()
    return key
def read_dec_db_file():
    with open(dec_file_name,'rb') as db:
        original = db.read()
    return original
def read_enc_db_file():
    with open(enc_file_name,'rb') as db:
        original = db.read()
    return original
def write_decrypted_db_file(dec_data):
    with open(dec_file_name, 'wb') as db_file:
        db_file.write(dec_data)
def delete_decrypted_db_file():
    os.remove(dec_file_name)
def write_encrypted_db_file(enc_data):
    with open(enc_file_name, 'wb') as db_file:
        db_file.write(enc_data)

def encrypt_db_with_key_and_store_in_file(data = None):
    _key = read_key()
    fern = fernet.Fernet(_key)
    if data==None:
        data = read_dec_db_file()
    encrypted_data = fern.encrypt(data)
    write_encrypted_db_file(encrypted_data)

def decrypt_db_with_key_and_create_temp_file():
    _key = read_key()
    fern = fernet.Fernet(_key)
    encrypted_data = read_enc_db_file()
    decrypted_data = fern.decrypt(encrypted_data)
    write_decrypted_db_file(decrypted_data)

