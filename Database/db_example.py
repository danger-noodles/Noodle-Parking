from Database.databaseClass import DatabaseClass

database = DatabaseClass()
## Voorbeeld van een select query
# nbplates = database.select("SELECT customer_numberplate FROM `parking_numberplates`")
#
# for plates in nbplates:
#     print(plates[0])

###Voorbeeld van een insert query
# database.insert("INSERT INTO `parking_numberplates`(`id`, `customer_id`, `customer_numberplate`) VALUES (NULL, 1, '4-FYA-A')")

###Voorbeeld van een update query
# database.update("UPDATE `parking_numberplates` SET `customer_numberplate`= '5-FYA-BA' WHERE `customer_id` = 1")

###Voorbeeld van een delete query
# database.delete("DELETE FROM `parking_numberplates` WHERE `customer_id` = 1")

# database.get_user_by_numberplate("4-FTA-23")
# database.get_customer_details_by_customer_id(1)

# numb = database.get_customer_id_by_numberplate('4-FYA-AA')
# print(numb)
#
# numb = database.get_customer_details_by_numberplate('4-FYA-AA')
# print(numb)

# numb = database.get_customer_history_by_numberplate('4-FYA-AA', 1)
# print(numb)
#
#
# asdf = database.get_customer_details_by_numberplate('4-FYA-AA')
# print(asdf)

# dddd = database.checkout(1)
# print(dddd)

# database.checkin('')

# details = database.get_customer_details_by_customer_id('1')
# print(details)
# print(details['customer_firstname'])

# database.insert_customer("Noortjuhh", "Poloooo", "Elzenlaan4", "3465TJ", "Man", "Driebruggen", "wouter@highserve.nl")

# boolb = database.get_customer_exists_by_numberplate('4-FYA-A')


#
# var2 = database.get_customer_details_by_customer_id('1')
# print(var2)

# database.checkin('9-ZZZ-AA', 'BENZINE', '1996', 'WOUTERAUTO', 'ENORM', 'BLAUW','6')
# db.checkin(info[0]['plate'], data['parking_car_fuel'], str.split(data['parking_car_releasedate'], '-')[0], data['parking_car_name'], data['parking_car_type'], data['parking_car_body'], str(data['parking_car_cylinder_capacity']))
database.checkout(6)

# print(bool)
### Closes the database connection
database.close_connection()
