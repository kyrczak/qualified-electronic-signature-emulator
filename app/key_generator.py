from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

def rsa_generate_key_pair():
    key = RSA.generate(4096)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key, private_key 

def save_key_to_file(key, filename):
    with open(filename, 'wb') as f:
        f.write(key)

def read_key_from_file(filename):
    with open(filename, 'rb') as f:
        key = f.read()
    return key

def aes_encryption(private_key, pin):
    aes_key = SHA256.new(pin.encode('utf-8')).digest()
    iv = get_random_bytes(16)

    cipher = AES.new(aes_key, AES.MODE_CFB, iv)
    padded_content = pad(private_key, 16)

    encrypted_content = cipher.encrypt(padded_content)
    result = iv + encrypted_content
    return result

def aes_decryption(encrypted_content, pin):
    aes_key = SHA256.new(pin.encode('utf-8')).digest()
    iv = encrypted_content[:16]
    encrypted_content = encrypted_content[16:]

    cipher = AES.new(aes_key, AES.MODE_CFB, iv)
    decrypted_content = cipher.decrypt(encrypted_content)
    unpadded_content = unpad(decrypted_content, 16)
    return unpadded_content