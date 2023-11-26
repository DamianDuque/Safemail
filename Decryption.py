from Crypto.Cipher import AES
from datetime import datetime
import json
import socket
import platform
import Correo
import base64


class FileDecryptor:
    def __init__(self, encrypted_filename, key, second_key, sender):
        self.encrypted_filename = encrypted_filename
        self.key = key
        self.sender = sender
        tempvar = encrypted_filename.split(".")
        self.decrypted_filename = tempvar[0]+"-dec."+tempvar[1]
        self.second_key = second_key
        self.state = None

    def setState(self, isSuccessful):
        if isSuccessful:
            self.state = "success"
        else:
            self.state = "fail"

    def decrypt(self):
        b2key = bytes(self.second_key, 'utf-8')
        found = False
        with open(self.encrypted_filename, 'rb') as file:
            nonce = file.read(16)
            tag = file.read(16)
            ciphertext = file.read()
            receptor = ciphertext.split(b'[SEPARATOR]')[0]
            receptor = base64.b64decode(receptor)
            ciphertext = ciphertext.split(b'[SEPARATOR]')[1]
        try:
            keyIndex = ciphertext.index(b2key)
            keySubIndex = ciphertext[keyIndex:].decode('utf-8')
            if self.second_key == keySubIndex:
                found = True
                ciphertext = ciphertext[:-len(b2key)]

        except:
            print("\033[0;31mIncorrect Second Key 1\033[0m")
            self.setState(found)
            return self.log_activity(), receptor

        clave_bytes = bytes.fromhex(self.key)
        cipher = AES.new(clave_bytes, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        with open("decripted"+self.encrypted_filename, 'wb') as file:
            file.write(plaintext)
        self.setState(found)
        if found is True:
            print("\033[0;32mSecond key Correct\033[0m")
        else:
            print("\033[0;31m[ERROR] Incorrect Second Key\033[0m")

        return self.log_activity(), receptor

    def log_activity(self):
        ip = socket.gethostbyname(socket.gethostname())
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        log_data = {
            'activity': 'DECRYPTION',
            'ip': ip,
            'user_email': self.sender,
            'timestamp': timestamp,
            'second_key': self.second_key,
            'state': self.state,
        }
        log_data_json = json.dumps(log_data, indent=4)

        with open('activity_log.json', 'a') as log_file:
            log_file.write(log_data_json + "\n")

        return log_data_json


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print(
            "\033[0;33mUse: python decryption.py <encrypted_file> <key> <second_key>\033[0m")
        sys.exit(1)

    encrypted_filename = sys.argv[1]
    # Convertir la clave en bytes desde una representación hexadecimal
    key = bytes.fromhex(sys.argv[2])
    second_key = sys.argv[3]

    decryptor = FileDecryptor(encrypted_filename, key, second_key)
    decryptor.decrypt()
