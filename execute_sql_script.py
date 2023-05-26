import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pandas as pd


# stablish connection with database
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


# execute query by function
def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        print("Query successful")
        return cursor
    except Error as err:
        print(f"Error: '{err}'")


def main():
    # stablishing connection
    conn = create_server_connection("localhost", "root", "password")

    # get queries from file
    queries = list()
    with open("file.txt", "r") as f:
        for line in f.read().split("\n")[::2]:
            queries.append(line)

    # execute queries
    for query in queries:
        execute_query(conn, query)


if __name__ == "__main__":
    main()
