from mysql.connector import connect

def dbconnect() -> object:
    return connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='userprofiles'
    )

def getprocess(sql: str, params: tuple = ()) -> list:
    db = dbconnect()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, params)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

def postprocess(sql: str, params: tuple = ()) -> bool:
    db = dbconnect()
    cursor = db.cursor()
    cursor.execute(sql, params)
    db.commit()
    success = cursor.rowcount > 0
    cursor.close()
    db.close()
    return success

def get_all_users() -> list:
    sql = "SELECT * FROM users"
    return getprocess(sql)

def get_user_by_idno(idno: str) -> dict:
    sql = "SELECT * FROM users WHERE idno = %s"
    params = (idno,)
    result = getprocess(sql, params)
    return result[0] if result else None

def add_user(idno, lastname, firstname, course, level, image_filename):
    query = """
    INSERT INTO users (idno, lastname, firstname, course, level, image)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (idno, lastname, firstname, course, level, image_filename)
    return postprocess(query, values)


