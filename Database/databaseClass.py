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

    def get_customer_id_by_numberplate(self, numberplate) -> dict:
        try:
            current.execute("SELECT `id` FROM `parking_numberplate` WHERE `numberplate` = '"+numberplate+"'")
            for data in current:

                select = data
            return select
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

    def get_customer_exists_by_numberplate(self, numberplate) -> bool:
        try:
            current.execute("SELECT COUNT(*) as number FROM `parking_numberplates` WHERE `customer_numberplate` = '"+numberplate+"'")
            for data in current:
                if (data['number'] == 0):
                    return False
                else:
                    return True
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
