from RDW.rdwClient import RdwClient


client = RdwClient()
# TODO: get licence plate from Cammile
data = client.fetch_by_plate('4-TFL-24')
if data:
    print(data)

    if client.validate_plate(data):
        # TODO: Connect this with Wouter's database
        print('Valid car')
    else:
        # TODO: connect this with Marco's GUI
        print('Wouter komt je stompen')
