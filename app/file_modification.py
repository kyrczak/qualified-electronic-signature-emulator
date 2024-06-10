from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
def rsa_encrypt(file, exported_key):
    """
    This function encrypts a file using RSA algorithm.

    :param file: The path to the file to be encrypted.
    :param exported_key: The public key to encrypt the file.
    """
    with open(file, 'rb') as f:
        data = f.read()
    public_key = RSA.import_key(exported_key)
    rsa = PKCS1_OAEP.new(public_key)
    cipher_file = rsa.encrypt(data)
    file_name = os.path.basename(file)
    print(file_name)
    print(os.path.dirname(file))
    dir_path = os.path.dirname(file) + "\\"
    if(dir_path == "\\"):
        dir_path = ""

    with open(f'{dir_path}encrypted_{file_name}', 'wb') as f:
        print(f'{dir_path}encrypted_{file_name}')
        f.write(cipher_file)

def rsa_decrypt(file, exported_key):
    """
    This function decrypts a file using RSA algorithm.

    :param file: The path to the file to be decrypted.
    :param exported_key: The private key to decrypt the file.
    """
    with open(file, 'rb') as f:
        data = f.read()
    private_key = RSA.import_key(exported_key)
    rsa = PKCS1_OAEP.new(private_key)
    plain_file = rsa.decrypt(data)
    file_name = os.path.basename(file)
    dir_path = os.path.dirname(file) + "\\"
    if(dir_path == "\\"):
        dir_path = ""

    with open(f'{dir_path}decrypted_{file_name}', 'wb') as f:
        f.write(plain_file)