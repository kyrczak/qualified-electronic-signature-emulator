from app.file_modification import *
from app.key_generator import *

def test_rsa_textfile():
    public_key, private_key = rsa_generate_key_pair()
    file = "test.txt"
    rsa_encrypt(file, public_key)
    rsa_decrypt(f"encrypted_{file}", private_key)
    data = open(file, 'rb').read()
    decrypted_data = open(f"decrypted_encrypted_{file}", 'rb').read()
    assert data == decrypted_data

def test_rsa_cppfile():
    public_key, private_key = rsa_generate_key_pair()
    file = "test_cpp.cpp"
    rsa_encrypt(file, public_key)
    rsa_decrypt(f"encrypted_{file}", private_key)
    data = open(file, 'rb').read()
    decrypted_data = open(f"decrypted_encrypted_{file}", 'rb').read()
    assert data == decrypted_data