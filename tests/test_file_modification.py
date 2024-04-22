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

def test_rsa_textfile_keys_in_files():
    PIN = "123"
    PUBLIC_KEY_LOCATION = "pub.bin"
    PRIVATE_KEY_LOCATION = "priv.bin"
    public_key = read_key_from_file(PUBLIC_KEY_LOCATION)
    private_key = read_key_from_file(PRIVATE_KEY_LOCATION)
    file = "test.txt"
    rsa_encrypt(file, public_key)
    rsa_decrypt(f"encrypted_{file}", aes_decryption(private_key,PIN))
    data = open(file, 'rb').read()
    decrypted_data = open(f"decrypted_encrypted_{file}", 'rb').read()
    assert data == decrypted_data   