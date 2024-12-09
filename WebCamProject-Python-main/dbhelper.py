import mysql.connector
from mysql.connector import Error

class Databasehelper:
    def __init__(self):
        # Update these with your MySQL credentials
        self.host = "localhost"
        self.user = "root"
        self.database = "students"

    def getdb_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                database=self.database
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def getprocess(self, sql: str):
        connection = self.getdb_connection()
        if not connection:
            return []
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    def postprocess(self, sql: str):
        connection = self.getdb_connection()
        if not connection:
            return False
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error executing query: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def getall_records(self, table: str):
        query = f"SELECT * FROM `{table}`"
        return self.getprocess(query)

    def find_record(self, table: str, idno: str):
        query = f"SELECT * FROM `{table}` WHERE `idno` = '{idno}'"
        return self.getprocess(query)

    def add_record(self, table: str, **kwargs):
        keys = kwargs.keys()
        values = kwargs.values()
        columns = ",".join(f"`{k}`" for k in keys)
        formatted_values = ",".join([f"'{v}'" if isinstance(v, str) else str(v) for v in values])
        query = f"INSERT INTO `{table}` ({columns}) VALUES ({formatted_values})"
        return self.postprocess(query)

    def update_record(self, table: str, **kwargs):
        keys = list(kwargs.keys())
        values = list(kwargs.values())
        fields = [f"`{keys[i]}` = '{values[i]}'" for i in range(1, len(keys))]
        set_clause = ", ".join(fields)
        query = f"UPDATE `{table}` SET {set_clause} WHERE `{keys[0]}` = '{values[0]}'"
        return self.postprocess(query)

    def delete_record(self, table: str, **kwargs):
        keys = list(kwargs.keys())
        values = list(kwargs.values())
        query = f"DELETE FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
        return self.postprocess(query)
