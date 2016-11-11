"""
    Author: Wouter Dijkstra
    Class: DatabaseClass

    This class contains functions to handle everything related to the database.
    We use the PyMySQL module to connect with the database. (https://github.com/PyMySQL/PyMySQL)
"""

#Imports
import pymysql
import time
from Utils.config import DB_HOST, DB_PASS, DB_USER, DB

#Create a connection to the database
connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             passwd=DB_PASS,
                             db=DB)
current = connection.cursor(pymysql.cursors.DictCursor)


class DatabaseClass:
    """
             Databaseclass containing all the functions
    """
    def close_connection(self):
        """
            Closed the database connection.
        """
        connection.close()

    def select(self, query) -> dict:
        """
            Function to use a SQL SELECT based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                select: dictionary with the data returned from the SQL query
        """
        try:
            current.execute(query)
            for data in current:
                select = data
            return select
        except Exception as error:
            print("Exception:", error)

    def insert(self, query):
        """
            Function to use a SQL INSERT based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                --
        """
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)

    def update(self, query):
        """
            Function to use a SQL UPDATE based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                --
        """

        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)

    def delete(self, query):
        """
            Function to use a SQL DELETE based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                --
        """
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)

    def get_customer_details_by_numberplate(self, numberplate) -> dict:
        """
            Function to get the customer details based on a given numberplate.

            Args:
                STRING: numberplate: numberplate from the numberplate recognition.
            Returns:
                DICT: with customer all the details from the database.
        """
        try:
            current.execute("SELECT pc.* FROM "
                            " `parking_customers` as pc,"
                            " `parking_numberplate` as pn,"
                            " `parking_numberplate_customer` as pnc "
                            " WHERE pc.customer_id = pnc.customer_id"
                            " AND pnc.numberplate_id = pn.id "
                            " AND pn.numberplate = '"+numberplate+"' LIMIT 1")
            for data in current:
                select = data
            return select
        except Exception as error:
            print("Exception:", error)

    def get_customer_history_by_numberplate(self, numberplate, limit) -> list:
        """
            Function to get the customer checkin history based on a given numberplate.

            Args:
                STRING: numberplate: numberplate from the numberplate recognition.
                INT: limit: how many history results you want returned. 1 will return the last checkin.
            Returns:
                dictionary with past checkin history from the database.
        """
        try:
            current.execute("SELECT ph.* FROM "
                            " `parking_numberplate` as pn,"
                            " `parking_history` as ph"
                            " WHERE pn.id = ph.parking_numberplate_id"
                            " AND pn.numberplate = '"+numberplate+"' LIMIT "+str(limit)+"")
            history = []
            for data in current:
                history.append(data)
            return history
        except Exception as error:
            print("Exception:", error)

    def insert_customer(self, firstname, lastname, address, postcode, sex, city, email):
        """
            Function to insert a customer into the database.

            Args:
                STRING: firstname
                STRING: lastname
                STRING: address
                STRING: postcode
                STRING: sex
                STRING: city
                STRING: email
            Returns:
                dictionary with customer all the details from the database.
        """
        try:
            with connection.cursor() as cursor:
                # Create a new record
                customer_join_date = int(time.time())
                query = ("INSERT INTO `parking_customers`("
                        " `customer_id`,"
                        " `customer_firstname`,"
                        " `customer_lastname`,"
                        " `customer_address`,"
                        " `customer_join_date`,"
                        " `customer_postcode`,"
                        " `customer_sex`,"
                        " `customer_city`,"
                        " `customer_email`"
                        ") VALUES (NULL, '{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')"\
                            .format(firstname, lastname, address, customer_join_date, postcode, sex, city, email))

                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)


    def checkin(self, parking_numberplate, parking_car_fuel, parking_car_releasedate, parking_car_name, parking_car_type, parking_car_body,parking_car_cylinder_capacity):
        """
            Function to checkin a car based on numberplate and some details about the car.

            Args:
                STRING: parking_numberplate: Numberplate of the car
                STRING: parking_car_fuel: Fuel type of the car
                STRING: parking_car_releasedate: Releasedate of the car (year)
                STRING: parking_car_name: Name of the car
                STRING: parking_car_type: Type of the car (Car, truck, van, etc)
                STRING: parking_car_body: Body of the car (coupe, SUV, etc)
                STRING: parking_car_cylinder_capacity: Capacity of the car cylinder
            Returns:
                --
        """
        try:
            with connection.cursor() as cursor:
                # Put a UNIX timestamp in parking_start
                parking_start = int(time.time())

                # Create a parking_id for the numberplate
                query = ("INSERT INTO `parking_numberplate`(`id`, `numberplate`) VALUES (NULL, '"+parking_numberplate+"')")
                cursor.execute(query)

                # Get the ID of the last inserted record
                parking_numberplate_id = connection.insert_id()

                query = ("INSERT INTO `parking_history`"
                         "(`parking_id`,"
                         " `parking_numberplate_id`,"
                         " `parking_start`,"
                         " `parking_stop`,"
                         " `parking_car_fuel`,"
                         " `parking_car_releasedate`,"
                         " `parking_car_name`,"
                         " `parking_car_type`,"
                         " `parking_car_body`,"
                         " `parking_car_cylinder_capacity`) "
                         "VALUES (NULL,'{0}','{1}',NULL,'{2}','{3}','{4}','{5}','{6}',{7})".format(parking_numberplate_id,
                                                                                             parking_start,
                                                                                             parking_car_fuel,
                                                                                             parking_car_releasedate,
                                                                                             parking_car_name,
                                                                                             parking_car_type,
                                                                                             parking_car_body,
                                                                                             parking_car_cylinder_capacity))
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)

    def checkout(self, parking_numberplate_id):
        """
            Function to checkout a car based on numberplate.
            Updates the parking_stop in the parking_history to a current timestamp.

            Args:
                INT: parking_numberplate_id: Numberplate of the car
            Returns:
                --
        """
        try:
            with connection.cursor() as cursor:
                parking_stop = int(time.time())
                # Create a new record
                cursor.execute("UPDATE `parking_history` SET `parking_stop`= "+str(parking_stop)+" WHERE `parking_numberplate_id` = "+str(parking_numberplate_id)+" ORDER BY parking_id DESC LIMIT 1")

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)
