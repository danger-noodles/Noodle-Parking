from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Utils.config import EMAIL_HOSTNAME, EMAIL_FROM_ADDRESS, EMAIL_POST, EMAIL_ACCOUNT, EMAIL_PASSWORD


class EmailSmtp:
    # Server
    host = EMAIL_HOSTNAME
    port = EMAIL_POST
    server = SMTP(host, port)

    from_address = EMAIL_FROM_ADDRESS
    to_address = None
    subject = None
    content = None

    def __init__(self, debug_level = 0):
        self.server.set_debuglevel(debug_level)

        self.server.ehlo()
        self.server.starttls()
        self.server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

    def set_to_address(self, address):
        self.to_address = address

    def set_content(self, content):
        self.content = content

    def set_subject(self, subject):
        self.subject = subject

    def send_mail(self):
        # Error exceptions
        if not self.content:
            raise ValueError('No message set')

        if not self.to_address:
            raise ValueError('No to address set')

        if not self.from_address:
            raise ValueError('No from address set')

        if not self.subject:
            raise ValueError('No subject set')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.from_address
        msg['To'] = self.to_address

        html = '''
        <html>
            <head></head>
            <body>
                ''' + self.content + '''
            </body>
        </html>
        '''

        msg.attach(MIMEText(html, 'html'))

        self.server.sendmail(self.from_address, self.to_address, msg.as_string())
        self.server.quit()
