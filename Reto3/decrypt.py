from Crypto.Cipher import AES
import json
import socket
import platform
from datetime import datetime

class FileDecryptor:
    def __init__(self, encrypted_filename, key, output_filename, second_key):
        self.encrypted_filename = encrypted_filename
        self.key = key
        self.output_filename = output_filename
        self.second_key = second_key

    def rebuild(self):
        fullfile = b''
        for i in range(encrypted_filename):
            with open("decrypted/"+str(i)+self.output_filename, 'rb') as f:
                fullfile+= f.read()

        fullfile = fullfile.decode("utf-8")
        fullfile = fullfile.split('\\\\n')
        with open("decrypted/"+"final"+self.output_filename, 'w') as finalfilne:
            for line in fullfile:
                finalfilne.write(line+'\n')


    def decrypt(self):
        b2key = bytes(self.second_key, 'utf-8')
        found = False
        for i in range(encrypted_filename):
            with open("encrypted/" + str(i)+"enc.txt", 'rb') as file:
                nonce = file.read(16)
                tag = file.read(16)
                ciphertext = file.read()
             
            try:
                keyString = ciphertext.index(b2key)
                keySubstring = ciphertext[keyString:]
                if self.second_key == keySubstring.decode('utf-8'):
                    found = True
                    ciphertext = ciphertext[:-len(b2key)]
            except:
                print("\033[0;31mIncorrect Second Key\033[0m")
                sys.exit()
            
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

            with open("decrypted/"+str(i)+self.output_filename, 'wb') as file:
                file.write(plaintext)

        if found == True:
            print("\033[0;32mSecond key Correct\033[0m")
        else:
            print("\033[0;31mIncorrect Second Key\033[0m")
            sys.exit()

        self.log_activity()
        self.rebuild()


    def log_activity(self):
        ip = socket.gethostbyname(socket.gethostname())
        computer_name = platform.node()
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        log_data = {
            'activity': 'DESENCRYPTOR',
            'ip': ip,
            'computer_name': computer_name,
            'timestamp': timestamp,
            'second_key': self.second_key,
        }

        with open('activity_log.json', 'a') as log_file:
            log_file.write(json.dumps(log_data, indent=4) + "\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Uso: python decryption.py <numero de archivos> <archivo_desencriptado> <clave> <segunda_llave>")
        sys.exit(1)

    encrypted_filename = int(sys.argv[1])
    output_filename = sys.argv[2]
    key = bytes.fromhex(sys.argv[3])  # Convertir la clave en bytes desde una representación hexadecimal
    second_key = sys.argv[4]

    decryptor = FileDecryptor(encrypted_filename, key, output_filename, second_key)
    decryptor.decrypt()