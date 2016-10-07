from Database.databaseClass import DatabaseClass

database = DatabaseClass()

nbplates = database.select("SELECT * FROM `parking_numberplates`")
for plates in nbplates:
    print(plates)


# numberplate = database.select("SELECT * FROM `parking_numberplates`")
# print(straw_message)
# for x in straw_message:
#     print(x)

# database.get_user_by_numberplate("4-FTA-23")
# database.get_customer_details_by_customer_id(1)
