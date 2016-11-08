from Database.databaseClass import DatabaseClass

database = DatabaseClass()
### Voorbeeld van een select query
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

# numb = database.get_customer_id_by_numberplate('4-FYA-A')
# print(numb)
#
# details = database.get_customer_details_by_customer_id('1')
# print(details)
#
# database.insert_customer("Noortjuhh", "Poloooo", "Elzenlaan4", "3465TJ", "Man", "Driebruggen", "wouter@highserve.nl")

### Closes the database connection
# database.close_connection()
