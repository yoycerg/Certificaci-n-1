import os
import pymysql
from pymysql.cursors import DictCursor


class MySQLConnection:
    def __init__(self, database):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=database,
            cursorclass=DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data or ())
            # los select devuelven filas, el resto devuelve el id
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            return cursor.lastrowid

    def close(self):
        self.connection.close()


def connectToMySQL(database):
    return MySQLConnection(database)
