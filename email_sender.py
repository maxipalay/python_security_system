# Tutorials followed:
#   how to send emails with python - section: Adding Attachments Using the email Package - https://realpython.com/python-send-email/#sending-a-plain-text-email
#   tip for timeouts when trying to send an email - https://stackoverflow.com/questions/49203706/is-there-a-way-to-prevent-smtp-connection-timeout-smtplib-python 
#
# Note: for email connection to work you need to allow less secure access on gmail
from time import sleep

# libraries for sending emails
import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self, email_server_address, email_server_port, email_address, email_password):
        self._email_server = email_server_address
        self._email_server_port = email_server_port
        self._email_address = email_address
        self._email_password = email_password
    
    def send_email(self, receiver_email, subject, body, filename):
        ''' Uses create_email_text to create a mail in the correct format and then tries to send it.'''
        content = self.__create_email_text(receiver_email, subject, body, filename)
        try:
            smtp_connection = self.__get_smtp_connection()
            smtp_connection.sendmail(self._email_address, receiver_email, content)
            smtp_connection.close()
        except Exception:
            sleep(.05)
            self.send_email(receiver_email, subject, body, filename)

    def __get_smtp_connection(self):
        # Create a secure SSL context
        context = ssl.create_default_context()
        # initialize the connection and log in
        server = smtplib.SMTP_SSL(self._email_server, self._email_server_port, context=context)
        server.login(self._email_address, self._email_password)
        return server

    def __create_email_text(self, receiver, subject, body, filename=None):
        ''' Create an email and encode it in the correct format. '''
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self._email_address
        message["To"] = receiver
        message["Subject"] = subject
        #message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))
    
        # Open file in binary mode
        if filename is not None:    # check if a filename has been passed
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

                # Encode file in ASCII characters to send by email    
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header("Content-Disposition",f"attachment; filename= {filename}",)

                # Add attachment to message and convert message to string
                message.attach(part)
        text = message.as_string()
        return text
