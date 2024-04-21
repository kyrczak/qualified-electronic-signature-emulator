from app.key_generator import *

def test_rsa_generate_key_pair():
    public_key, private_key = rsa_generate_key_pair()
    assert public_key
    assert private_key

def test_save_key_to_file(tmp_path):
    key = b'key'
    filename = tmp_path / 'key'
    save_key_to_file(key, filename)
    assert filename.read_bytes() == key

def test_aes_encrypt_decrypt():
    message = b'message'
    pin = '1234'
    encrypted_content = aes_encryption(message, pin)
    decrypted_content = aes_decryption(encrypted_content, pin)
    assert decrypted_content == message

# Run the test
# $ pytest test_key_generator.py