from Utils.config import RDW_STOMP_EMAIL
from RDW.rdwClient import RdwClient
from Utils.emailSMTP import EmailSmtp


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
email_server.send_stomp_mail()
email_server.quit()
