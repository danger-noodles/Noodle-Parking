'''' Author: Wouter Dijkstra '''

import pymysql
import time
from Utils.config import DB_HOST, DB_PASS, DB_USER, DB
connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             passwd=DB_PASS,
                             db=DB)
current = connection.cursor(pymysql.cursors.DictCursor)

class DatabaseClass:
    def close_connection(self):
            connection.close()

    def select(self, query) -> dict:
        try:
            current.execute(query)
            for data in current:
                select = data
            return select
        except Exception as error:
            print("Exception:", error)

    def insert(self, query):
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
        try:
            with connection.cursor() as cursor:
                # Create a new record
                parking_start = int(time.time())

                query = ("INSERT INTO `parking_numberplate`(`id`, `numberplate`) VALUES (NULL, '"+parking_numberplate+"')")
                cursor.execute(query)

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
                         "VALUES (NULL,'{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(parking_numberplate_id,
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
