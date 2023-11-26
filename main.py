from Crypto.Random import get_random_bytes
import Decryption
import Encryption
import Correo
import re
import os


def is_not_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is None


if __name__ == "__main__":
    import sys

    # Accion de enviar:
    if len(sys.argv) < 2:
        print("\033[0;33mPlease specify an action: send or decrypt\033[0m")
        sys.exit(1)

    if sys.argv[1] == "send":
        if len(sys.argv) != 9:
            print(
                "\033[0;33mUse: python main.py send <file_to_send> <sender_email> <receiver_email> <auth_key>\033[0m")
            sys.exit(1)

        filename = sys.argv[2]
        sender = sys.argv[3]
        receiver = sys.argv[4]
        auth_key = sys.argv[5]+" "+sys.argv[6]+" "+sys.argv[7]+" "+sys.argv[8]

        try:
            with open(filename):
                print("File to encrypt: "+filename+"...")
        except FileNotFoundError:
            print("\033[0;31m[ERROR] File to encrypt: "+filename +
                  " not in the main directory or doesn't exist\033[0m")
            sys.exit()
        if is_not_email(sender):
            print("\033[0;31m[ERROR] Incorrect Sender Email Format\033[0m")
            sys.exit()
        elif is_not_email(receiver):
            print("\033[0;31m[ERROR] Incorrect Receiver Email Format\033[0m")
            sys.exit()

        key = get_random_bytes(16)
        key_hex = key.hex()
        second_key = receiver.split("@")[0]
        encriptor = Encryption.FileEncryptor(filename, key, second_key)
        outputfile = encriptor.encrypt(sender)

        email = Correo.Mail(sender, receiver)
        email.sendFirstMail(outputfile, "Encrypted File",
                            "Hi there! This is the encrypted file sent by "+sender+".", auth_key)
        email.sendSecondMail(key_hex, auth_key)

    if sys.argv[1] == "decrypt":
        if len(sys.argv) != 10:
            print(
                "\033[0;33mUse: python main.py decrypt <received_file> <key> <my_mail> <second_key> <auth_key>\033[0m")
            sys.exit(1)

        filename = sys.argv[2]
        try:
            with open(filename):
                print("🎄 \033[0;32mFile to decrypt: \033[0m" +
                      "\033[0;31m"+filename+"...\033[0m 🎄")
        except FileNotFoundError:
            print("\033[0;31m[ERROR] File to decrypt: "+filename +
                  " not in the main directory or doesn't exist\033[0m")
            sys.exit()
        key = sys.argv[3]
        sender = sys.argv[4]
        second_key = sys.argv[5]
        auth_key = sys.argv[6]+" "+sys.argv[7]+" "+sys.argv[8]+" "+sys.argv[9]

        if is_not_email(sender):
            print("\033[0;31m[ERROR] Incorrect Sender Email Format\033[0m")
            sys.exit()
        else:
            decryptor = Decryption.FileDecryptor(
                filename, key, second_key, sender)
            logdata, receiver = decryptor.decrypt()
            email = Correo.Mail(sender, receiver.decode("utf-8"))
            email.sendFirstMail("", "Log Activity", logdata, auth_key)
