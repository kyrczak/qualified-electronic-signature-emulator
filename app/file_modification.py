from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def rsa_encrypt(file, exported_key):
    with open(file, 'rb') as f:
        data = f.read()
    public_key = RSA.import_key(exported_key)
    rsa = PKCS1_OAEP.new(public_key)
    cipher_file = rsa.encrypt(data)
    with open(f'encrypted_{file}', 'wb') as f:
        f.write(cipher_file)

def rsa_decrypt(file, exportet_key):
    with open(file, 'rb') as f:
        data = f.read()
    private_key = RSA.import_key(exportet_key)
    rsa = PKCS1_OAEP.new(private_key)
    plain_file = rsa.decrypt(data)
    with open(f'decrypted_{file}', 'wb') as f:
        f.write(plain_file)