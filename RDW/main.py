from Utils.config import RDW_STOMP_EMAIL
from RDW.rdwClient import RdwClient
from Utils.emailSMTP import EmailSmtp
import time


# client = RdwClient()
# # TODO: get licence plate from Cammile
# # fetch the data
# client.fetch_by_plate('4-TFL-24')
# if client.validate_plate():
#     # TODO: Connect this with Wouter's database
#     print('Valid car')
# else:
#     # TODO: connect this with Marco's GUI
#     print('Wouter komt je stompen')

email_server = EmailSmtp()

email_server.set_subject('Diesel auto probeerd in te checken')
email_server.set_to_address(RDW_STOMP_EMAIL)
# email_server.send_stomp_mail()
invoice_data = {
    'id': 1337,
    'date': time.time(),
    'due_date': time.time(),
    'description': 'Parking noodle parkeer garage',
    'price': time.time() * 0.6,
    'client': {
        'address': 'Sesam straat 3',
        'country': 'Nederland',
        'city': 'Uitweg',
        'name': 'Harry baksel',
        'zip-code': '1337 LD'
    }
}
email_server.send_invoice_mail(invoice_data)
email_server.quit()
