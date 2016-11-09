from Utils.config import RDW_STOMP_EMAIL
from RDW.rdwClient import RdwClient
from Utils.emailSMTP import EmailSmtp

client = RdwClient()
email_server = EmailSmtp()

# TODO: get licence plate from Cammile
# fetch the data
# if client.fetch_by_plate('4-TFL-24'):
if client.fetch_by_plate('94-NDL-5'):
    if client.validate_plate():
        # TODO: Connect this with Wouter's database
        print('Valid car')
    else:
        email_server.set_subject('Diesel auto probeerd in te checken')
        email_server.set_to_address(RDW_STOMP_EMAIL)
        email_server.send_stomp_mail()
        print('Wouter komt je stompen')
else:
    print('Api error: Licence plate could not found')

email_server.quit()
