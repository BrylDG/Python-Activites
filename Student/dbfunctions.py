from sqlite3 import connect, Row

database: str = "student.db"

def postprocess(sql: str) -> bool:
    db: object = connect(database)
    cursor: object = db.cursor()
    cursor.execute(sql)
    db.commit()
    rowcount = cursor.rowcount
    cursor.close()
    return True if rowcount > 0 else False

def getprocess(sql: str) -> list:
    db: object = connect(database)
    cursor: object = db.cursor()
    cursor.row_factory = Row
    cursor.execute(sql)
    data: list = cursor.fetchall()
    cursor.close()
    return data
    
def getall_records(table:str)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql)

def add_record(table: str, **kwargs) -> bool:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    fields: str = "`,`".join(keys)
    data: str = "','".join(values)
    sql: str = f"INSERT INTO `{table}`(`{fields}`) VALUES('{data}')"
    return postprocess(sql)
