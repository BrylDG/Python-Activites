from sqlite3 import connect, Row

database = "books.db"

def postprocess(sql: str) -> bool:
    db = connect(database)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    rowcount = cursor.rowcount
    cursor.close()
    return rowcount > 0

def getprocess(sql: str) -> list:
    db = connect(database)
    cursor = db.cursor()
    cursor.row_factory = Row
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data

def getall_records(table: str) -> list:
    sql = f"SELECT * FROM `{table}`"
    return getprocess(sql)

def add_record(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    fields = "`,`".join(keys)
    data = "','".join(values)
 
    if validate_record(table, kwargs.get('isbn')):
        return False 

    sql = f"INSERT INTO `{table}`(`{fields}`) VALUES('{data}')"
    return postprocess(sql)

def validate_record(table: str, isbn: str) -> bool:
    sql = f"SELECT COUNT(*) FROM `{table}` WHERE isbn = ?"
    db = connect(database)
    cursor = db.cursor()
    cursor.execute(sql, (isbn,))
    result = cursor.fetchone()[0]
    cursor.close()
    return result > 0
