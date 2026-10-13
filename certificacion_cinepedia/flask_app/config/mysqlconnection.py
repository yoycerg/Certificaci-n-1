import pymysql
from pymysql.cursors import DictCursor


class MySQLConnection:
    def __init__(self, database):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database=database,
            cursorclass=DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, data or ())
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            return cursor.lastrowid

    def close(self):
        self.connection.close()


def connectToMySQL(database):
    return MySQLConnection(database)
