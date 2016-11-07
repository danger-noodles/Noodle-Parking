from RDW.rdwClient import RdwClient


client = RdwClient()
# TODO: get licence plate from Cammile
# fetch the data
if client.fetch_by_plate('4-TFL-24'):
    if client.validate_plate():
        # TODO: Connect this with Wouter's database
        print('Valid car')
    else:
        # TODO: connect this with Marco's GUI
        print('Wouter komt je stompen')
else:
    print('Invalid plate')
