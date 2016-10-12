'''' Authoer: Wouter Dijkstra '''

import pymysql
import time
from Utils.config import DB_HOST, DB_PASS, DB_USER, DB
connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             passwd=DB_PASS,
                             db=DB)
current = connection.cursor()

class DatabaseClass:
    def select(self, query) -> list:
        try:
            current.execute(query)
            select = []
            for data in current:
                select.append(data)
            return select
        finally:
            connection.close()

    def insert(self, query):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        finally:
            connection.close()

    def update(self, query):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        finally:
            connection.close()

    def delete(self, query):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        finally:
            connection.close()

    def get_customer_id_by_numberplate(self, numberplate) -> list:
        try:
            current.execute("SELECT `customer_id` FROM `parking_numberplates` WHERE `customer_numberplate` ="+numberplate)
            select = []
            for data in current:
                select.append(data)
            return select
        finally:
            connection.close()

    def get_customer_details_by_customer_id(self, customer_id) -> list:
        try:
            current.execute("SELECT * FROM `parking_customers` WHERE `customer_id` ="+customer_id)
            select = []
            for data in current:
                select.append(data)
            return select
        finally:
            connection.close()

    def insert_customer(self, firstname, lastname, address):
        try:
            customer_join_date = time.time()
            current.execute("INSERT INTO `parking_customers`("
                            " `customer_id`,"
                            " `customer_firstname`,"
                            " `customer_lastname`,"
                            " `customer_address`,"
                            " `customer_join_date`,"
                            "VALUES (NULL, '{0}','{1}','{2}','{3}')".format(firstname, lastname, address, customer_join_date))
        finally:
            connection.close()
