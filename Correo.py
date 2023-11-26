from email.message import EmailMessage
import ssl
import smtplib
import os
import sys


class Mail:
    def __init__(self, email_sender, email_receiver):
        self.sender = email_sender
        self.receiver = email_receiver

    def sendFirstMail(self, file_name, subject, body, password):
        """email_sender = 'damianduquel@gmail.com'
        email_password = 'bopz wsma rdmj lqwy'
        email_receiver = 'estebantrujillocarmona@gmail.com'"""

        '''subject = "Encrypted File"
        body = "Body"'''
        email_password = password

        em = EmailMessage()
        em['From'] = self.sender
        em['To'] = self.receiver
        em['subject'] = subject
        em.set_content(body)

        if file_name != "":
            try:
                file_path = os.path.abspath(file_name)

                with open(file_path, 'rb') as file:
                    em.add_attachment(
                        file.read(), maintype='application', subtype='octet-stream', filename=file_name)
            except:
                print("\033[0;31m[ERROR] File Does Not Exist\033[0m")
                sys.exit()
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.sender, email_password)
            smtp.sendmail(self.sender, self.receiver, em.as_string())

    def sendSecondMail(self, key, email_password):

        em = EmailMessage()
        em['From'] = self.sender
        em['To'] = self.receiver
        em['subject'] = "First file decryption key"
        body = "The key is: " + str(key)
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.sender, email_password)
            smtp.sendmail(self.sender, self.receiver, em.as_string())
