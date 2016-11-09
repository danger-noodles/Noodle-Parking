from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
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

    def send_stomp_mail(self):
        self.set_content('''
            Geachte heer dijkstra,


            Iemand heeft zojuist geprobeerd in te checken met een diesel auto waarvan de laatste aangifte van voor 2001 is.
            Wij hopen dat u zo spoedig mogelijk actie onderneemt.
        '''.replace('\n', '<br />'))
        self.send_mail()

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

        msg_root = MIMEMultipart('related')
        msg_root['Subject'] = self.subject
        msg_root['From'] = self.from_address
        msg_root['To'] = self.to_address
        msg_root.preamble = 'This is a multi-part message in MIME format.'

        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)

        html = self.content + '''
            Met Vriendelijke Groet,


            Danger Noodles
            <img src="cid:snek.jpg" alt="Snek logo.jpg" />
        '''.replace('\n', '<br />')

        msg_alternative.attach(MIMEText(html, 'html'))

        # image
        fp = open('../Utils/snek.jpg', 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()
        # Define the image's ID as referenced above
        msg_image.add_header('Content-ID', '<snek.jpg>')
        msg_root.attach(msg_image)

        self.server.sendmail(self.from_address, self.to_address, msg_root.as_string())
        # print(msg.as_string())

    def quit(self):
        self.server.quit()
