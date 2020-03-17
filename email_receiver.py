# Tutorials followed:
#   how to receive emails with python/imap - https://pypi.org/project/imap-tools/
#
# Note: for email connection to work you need to allow less secure access on gmail

# libraries for receiving emails
from imap_tools import MailBox, Q

class EmailReceiver:
    def __init__(self, email_server_address, email_address, email_password):
        self._email_server = email_server_address
        self._email_address = email_address
        self._email_password = email_password

    def get_new_emails(self):
        ''' Checks for new email. If there is new email, it will return the tuple (sender, subject)'''
        # I suppose one email will have been received, otherwise just pick the last email received
        try:
            mailbox = MailBox(self._email_server)
            mailbox.login(self._email_address, self._email_password, initial_folder='INBOX')
            received_emails = False
            subject = None
            sender = None
            for msg in mailbox.fetch(Q(seen=False)):
                received_emails = True
                subject = msg.subject.lower()
                sender = msg.from_
                #print(subject)
            mailbox.logout()
        except Exception:
            print("Some error occured while checking for new emails...")
            return (None, None)
        if received_emails:
            return (sender, subject)
        else:
            return (None,None)

