from Crypto.Random import get_random_bytes
import Decryption
import Encryption
import Correo


def enviar():
    pass

def recepcion():
    pass

def registro():
    pass


if __name__ == "__main__":
    import sys

    #Accion de enviar:
    if len(sys.argv) < 2:
        print("Porfavor indique que accion desea realizar")
        
    if sys.argv[1] == "send":
        if len(sys.argv) != 5:
            print("Uso: python main.py send <archivo_a_enviar> <correo_de_envio> <correo_destino>")
            sys.exit(1)
        #Suerte! :)
        #Gracias! :)
        filename = sys.argv[2]
        
        sender = sys.argv[3]
        receiver = sys.argv[4]
        if "@" not in receiver and sender:
            print("\033[0;31mIncorrect Emails\033[0m")
            sys.exit()
        key = get_random_bytes(16)
        key_hex = key.hex()
        second_key = receiver.split("@")[0]
        print(second_key)
        encriptor = Encryption.FileEncryptor(filename, key, second_key)
        outputfile = encriptor.encrypt()

        email = Correo.Mail(sender, receiver)
        email.sendFirstMail(outputfile)
        email.sendSecondMail(key_hex)

    if sys.argv[1] == "decrypt":
        if len(sys.argv) != 5:
            print("Uso: python main.py decrypt <archivo_recibido> <clave> <correo_destinatario> <correo_origen>")
            sys.exit(1)
        #Suerte! :)
        #Gracias! :)
        filename = sys.argv[2]
        key = sys.argv[3]
        sender = sys.argv[4]
        receiver = sys.argv[5]
        if "@" not in receiver and sender:
            print("\033[0;31mIncorrect Emails\033[0m")
            sys.exit()
        decryptor = Decryption.FileDecryptor(filename, key, second_key)
        logdata, outputfile = decryptor.decrypt()
        print(logdata)
        print(outputfile)

        email = Correo.Mail(sender, receiver)
        email.sendLogMail(logdata)
        


        