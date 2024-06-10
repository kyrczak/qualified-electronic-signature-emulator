from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

def rsa_generate_key_pair():
    """ 
    This function generates the RSA key pair.
    
    :return: The public and private key.
    """
    key = RSA.generate(4096)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key, private_key 

def save_key_to_file(key, filename):
    """
    This function saves a key to a file.
    
    :param key: The key to be saved.
    :param filename: The path to the file where the key will be saved.
    """
    with open(filename, 'wb') as f:
        f.write(key)

def read_key_from_file(filename, pin = None):
    """
    This function reads a key from a file.

    :param filename: The path to the file where the key is saved.
    :param pin: The pin to decrypt the key.
    """
    with open(filename, 'rb') as f:
        key = f.read()
        if(pin != None):
            key = aes_decryption(key,pin)
    return key

def aes_encryption(private_key, pin):
    """
    This function encrypts a private key using AES encryption.
    
    :param private_key: The private key to be encrypted.
    :param pin: The pin to encrypt the private key.
    """
    aes_key = SHA256.new(pin.encode('utf-8')).digest()
    iv = get_random_bytes(16)

    cipher = AES.new(aes_key, AES.MODE_CFB, iv)
    padded_content = pad(private_key, 16)

    encrypted_content = cipher.encrypt(padded_content)
    result = iv + encrypted_content
    return result

def aes_decryption(encrypted_content, pin):
    """
    This function decrypts a private key using AES encryption.

    :param encrypted_content: The encrypted private key.
    :param pin: The pin to decrypt the private key.
    """
    aes_key = SHA256.new(pin.encode('utf-8')).digest()
    iv = encrypted_content[:16]
    encrypted_content = encrypted_content[16:]

    cipher = AES.new(aes_key, AES.MODE_CFB, iv)
    decrypted_content = cipher.decrypt(encrypted_content)
    unpadded_content = unpad(decrypted_content, 16)
    return unpadded_content