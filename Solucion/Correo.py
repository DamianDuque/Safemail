from email.message import EmailMessage
import ssl
import smtplib
import os

class Mail:
    def __init__(self, email_sender, email_receiver):
        self.sender = email_sender
        self.receiver = email_receiver
        
    def sendFirstMail(self, file_name):
        """email_sender = 'damianduquel@gmail.com'
        email_password = 'bopz wsma rdmj lqwy'
        email_receiver = 'estebantrujillocarmona@gmail.com'"""

        '''subject = "Encrypted File"
        body = "Body"'''
        email_password = 'bopz wsma rdmj lqwy'

        em = EmailMessage()
        em['From'] = self.sender
        em['To'] = self.receiver
        em['subject'] = "File sent by "+ self.sender
        body = ""
        em.set_content(body)
        
        if file_name != "":
            file_path = os.path.abspath(file_name)

            with open(file_path, 'rb') as file:
                em.add_attachment(file.read(), maintype='application', subtype='octet-stream', filename=file_name)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.sender, email_password)
            smtp.sendmail(self.sender, self.receiver, em.as_string())


    def sendSecondMail(self, key):
        email_password = 'bopz wsma rdmj lqwy'

        em = EmailMessage()
        em['From'] = self.sender
        em['To'] = self.receiver
        em['subject'] = "First file decryption key"
        body = "The key is: " +str(key)
        em.set_content(body)
        
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.sender, email_password)
            smtp.sendmail(self.sender, self.receiver, em.as_string())


    def sendLogMail(self, log_data):
        email_password = 'bopz wsma rdmj lqwy'

        em = EmailMessage()
        em['From'] = self.sender
        em['To'] = self.receiver
        em['subject'] = "The user decrypted your file!"
        datastr = ""
        for key, value in datastr.items():
            datastr += f"{key}: {value}, "
            
        em.set_content(datastr)
        
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.sender, email_password)
            smtp.sendmail(self.sender, self.receiver, em.as_string())