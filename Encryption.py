import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import socket
import platform
from datetime import datetime
import base64
import sys


class FileEncryptor:
    def __init__(self, filename, key, second_key):
        self.filename = filename
        self.key = key
        tempvar = filename.split(".")
        self.output_filename = tempvar[0] + "-enc." + tempvar[1]
        self.second_key = second_key

    def encrypt(self, sender):

        cipher = AES.new(self.key, AES.MODE_EAX)
        with open(self.filename, 'rb') as file:
            plaintext = file.read()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        b2key = bytes(self.second_key, 'utf-8')
        sender_bytes = bytes(sender, 'utf-8')

        with open(self.output_filename, 'wb') as file:

            file.write(cipher.nonce)
            file.write(tag)
            file.write(base64.b64encode(sender_bytes)+b'[SEPARATOR]')
            file.write(ciphertext)
            file.write(b2key)

        self.log_activity()
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=cipher.nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
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

    if len(sys.argv) != 3:
        print(
            "\033[0;31mUso: py encryption.py <archivo_a_encriptar> <segunda_llave>\033[0m")
        sys.exit(1)

    filename = sys.argv[1]
    key = get_random_bytes(16)
    second_key = sys.argv[2]
    clave = "bopz wsma rdmj lqwy"
    encryptor = FileEncryptor(filename, key, second_key, clave)
    # encryptor.encrypt()
