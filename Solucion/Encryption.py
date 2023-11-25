import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import socket
import platform
from datetime import datetime

class FileEncryptor:
    def __init__(self, filename, key, second_key):
        self.filename = filename
        self.key = key
        tempvar = filename.split(".")
        self.output_filename = tempvar[0] + "-enc." + tempvar[1]
        self.second_key = second_key

    def encrypt(self):
        cipher = AES.new(self.key, AES.MODE_EAX)
        with open(self.filename, 'rb') as file:
            plaintext = file.read()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        b2key = bytes(self.second_key, 'utf-8')
        with open(self.output_filename, 'wb') as file:
            file.write(cipher.nonce)
            file.write(tag)
            file.write(ciphertext)
            file.write(b2key)

        self.log_activity()
        return self.output_filename

    def log_activity(self):
        ip = socket.gethostbyname(socket.gethostname())
        computer_name = platform.node()
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        key_hex = self.key.hex()  # Convierte la clave en una cadena hexadecimal
        
        log_data = {
            'activity': 'ENCRYPTOR',
            'ip': ip,
            'computer_name': computer_name,
            'timestamp': timestamp,
            'key': key_hex,
            'second_key': self.second_key,
        }

        with open('activity_log.json', 'a') as log_file:
            log_file.write(json.dumps(log_data, indent=4) + "\n")

if __name__ == "__main__":

    import sys

    if len(sys.argv) != 4:
        print("Uso: py encryption.py <archivo_a_encriptar> <archivo_encriptado> <segunda_llave>")
        sys.exit(1)

    filename = sys.argv[1]
    output_filename = sys.argv[2]
    key = get_random_bytes(16)
    second_key = sys.argv[3]

    encryptor = FileEncryptor(filename, key, output_filename, second_key)
    encryptor.encrypt()