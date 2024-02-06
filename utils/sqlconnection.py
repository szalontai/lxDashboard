import urllib.parse

import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from utils.config import settings
from utils.queryfetchtype_enum import QueryFetchType

baseConnString = (
    "DRIVER="
    + settings.sql_odbc_driver
    + ";SERVER="
    + settings.sql_server_name
    + ","
    + settings.sql_server_port
    + ";DATABASE="
    + settings.sql_database
    + ";ENCRYPT=no;"
)
connString = baseConnString + "UID=" + settings.sql_username + ";PWD="
url_db = urllib.parse.quote_plus(connString + urllib.parse.quote(settings.sql_password))
engine = create_engine(
    "mssql+pyodbc:///?odbc_connect=%s" % url_db, echo=settings.sql_echo
)


def return_data(data, cursor):
    columns = [column[0] for column in cursor.description]
    return data, columns


class SqlConnection:
    def execute_query(self, query, fetch_type: QueryFetchType, connection=""):
        connection_string = connString + settings.sql_password
        if connection:
            connection_string = connection

        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        cursor.execute(query)
        data = []

        if fetch_type == QueryFetchType.ALL:
            data = cursor.fetchall()
        else:
            data = cursor.fetchone()

        cnxn.close()
        return return_data(data, cursor)

    def get_session(self):
        return Session(engine)

    def validate_user(self, user, password):
        conn = baseConnString + "UID=" + user + ";PWD=" + password
        query = " SELECT TOP 1 * FROM USERS WHERE USUARIO ='" + user + "'"
        return self.execute_query(query, QueryFetchType.ONE, conn)
