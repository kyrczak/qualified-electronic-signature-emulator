import key_generator

def test_rsa_generate_key_pair():
    public_key, private_key = key_generator.rsa_generate_key_pair()
    assert public_key
    assert private_key

def test_save_key_to_file(tmp_path):
    key = b'key'
    filename = tmp_path / 'key'
    key_generator.save_key_to_file(key, filename)
    assert filename.read_bytes() == key

def test_aes_encrypt_decrypt():
    message = b'message'
    pin = '1234'
    encrypted_content = key_generator.aes_encryption(message, pin)
    decrypted_content = key_generator.aes_decryption(encrypted_content, pin)
    assert decrypted_content == message

# Run the test
# $ pytest test_key_generator.py