from smtplib import SMTP
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from Utils.config import EMAIL_HOSTNAME, EMAIL_FROM_ADDRESS, EMAIL_POST, EMAIL_ACCOUNT, EMAIL_PASSWORD


class EmailSmtp:
    """
        Author: Nick Bout
        Class: EmailSmtp
        This class uses the smtplib library to send emails
    """
    # Server
    host = EMAIL_HOSTNAME
    port = EMAIL_POST
    server = SMTP(host, port)

    from_address = EMAIL_FROM_ADDRESS
    to_address = None
    subject = None
    content = None

    def __init__(self, debug_level = 0):
        """
            Constructor function

            ARGS:
                debug_level INT: debug level for the smtplib || Default value 0
        """
        self.server.set_debuglevel(debug_level)

        self.server.ehlo()
        self.server.starttls()
        self.server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

    def set_to_address(self, address):
        """
            Setter function for to_address

            ARGS:
                address STRING: the receiving email
            RETURNS:
                --
        """
        self.to_address = address

    def set_content(self, content):
        """
            Setter function for content

            ARGS:
                content STRING: Content for the email
            RETURNS:
                --
        """
        self.content = content

    def set_subject(self, subject):
        """
            Setter function for subject

            ARGS:
                subject STRING: Email subject
            RETURNS:
                --
        """
        self.subject = subject

    def send_invoice_mail(self, invoice_data):
        """
            Function to send invoice email

            ARGS:
                invoice_data DICT: Dictionary with all data needed for the invoice
            RETURNS:
                --
        """
        self.set_content('''
            Factuur voor:<br />
            ''' + invoice_data['client']['name'] + '''<br />
            ''' + invoice_data['client']['address'] + '''<br />
            ''' + invoice_data['client']['city'] + ''',''' + invoice_data['client']['zip-code'] + ''',''' + invoice_data['client']['country'] + '''<br /><br />
            <h1>FACTUUR</h1>
            <hr>
            <table>
                <tbody>
                    <tr>
                        <td>Factuur Nr:</td>
                        <td>''' + str(invoice_data['id']) + '''<td>
                    </tr>
                    <tr>
                        <td>Date:</td>
                        <td>''' + datetime.fromtimestamp(invoice_data['date']).strftime('%Y-%m-%d') + '''<td>
                    </tr>
                    <tr>
                        <td>Date:</td>
                        <td>''' + datetime.fromtimestamp(invoice_data['due_date']).strftime('%Y-%m-%d') + '''<td>
                    </tr>
                    <tr>
                        <td>DESCRIPTION</td>
                        <td>''' + invoice_data['description'] + '''<td>
                    </tr>
                    <tr>
                        <td>PRICE<td>
                        <td>''' + str(invoice_data['price']) + '''<td>
                    </tr>
                </tbody>
            </table>
            <br />
            <b>Payment terms:</b> Payment within ''' + str((datetime.fromtimestamp(invoice_data['due_date']) - datetime.fromtimestamp(invoice_data['date'])).days) + ''' days<br />
            <b>Payment details:</b><br />
            Money transfer to the account below:<br />
            <br />
            <table>
                <tbody>
                    <tr>
                        <td>Bank:</td>
                        <td>ING bank</td>
                    </tr>
                    <tr>
                        <td>IBAN:</td>
                        <td>NL99 ING 1337 1414 69</td>
                    </tr>
                    <tr>
                        <td>Payment Reference:</td>
                        <td>''' + str(invoice_data['id']) + '''</td>
                    </tr>
                </tbody>
            </table>
        ''')
        self.send_mail()

    def send_stomp_mail(self):
        """
            Function to send stomp email

            ARGS:
                --
            RETURNS:
                --
        """
        self.set_content('''
            Geachte heer Dijkstra,

            Iemand heeft zojuist geprobeerd in te checken met een diesel auto waarvan de laatste aangifte van voor 2001 is.
            Wij hopen dat u zo spoedig mogelijk actie onderneemt.
        '''.replace('\n', '<br />'))
        self.send_mail()

    def send_mail(self):
        """
            Function to a send email, this uses its own variables set with the setters

            ARGS:
                --
            RETURNS:
                --
        """
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
        fp = open('./Utils/snek.jpg', 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()
        # Define the image's ID as referenced above
        msg_image.add_header('Content-ID', '<snek.jpg>')
        msg_root.attach(msg_image)

        self.server.sendmail(self.from_address, self.to_address, msg_root.as_string())

    def quit(self):
        """
            Function to quit server connection

            ARGS:
                --
            RETURNS:
                --
        """
        self.server.quit()
