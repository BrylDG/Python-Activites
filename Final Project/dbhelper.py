### dbhelper.py (Refactored and Consolidated Database Helper)
from mysql.connector import connect

# Database connection configuration
def dbconnect() -> object:
    return connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='users'  # Ensure unified database name
    )

# Execute SELECT queries with parameterized inputs
def getprocess(sql: str, params: tuple = ()) -> list:
    db = dbconnect()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, params)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

# Execute INSERT/UPDATE/DELETE queries with parameterized inputs
def postprocess(sql: str, params: tuple = ()) -> bool:
    db = dbconnect()
    cursor = db.cursor()
    cursor.execute(sql, params)
    db.commit()
    success = cursor.rowcount > 0
    cursor.close()
    db.close()
    return success

# Fetch all records from a table
def get_all_records(table: str) -> list:
    sql = f"SELECT * FROM `{table}`"
    return getprocess(sql)

# Add a new user
def add_user(idno: str, lastname: str, firstname: str, course: str, level: str, image: str, qr_filename: str) -> bool:
    sql = """
        INSERT INTO `students` (`idno`, `lastname`, `firstname`, `course`, `level`, `image`, `qr_filename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (idno, lastname, firstname, course, level, image, qr_filename)
    return postprocess(sql, params)

# Validate user credentials
def validate_user(username: str, password: str) -> list:
    sql = "SELECT * FROM `users` WHERE `username`= %s AND `password`= %s"
    params = (username, password)
    return getprocess(sql, params)

# Get user by ID number
def get_user_by_idno(idno: str) -> dict:
    sql = "SELECT * FROM `students` WHERE `idno` = %s"
    params = (idno,)
    result = getprocess(sql, params)
    return result[0] if result else None

# Get all users
def get_all_users() -> list:
    sql = "SELECT * FROM students"
    return getprocess(sql)