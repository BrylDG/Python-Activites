from mysql.connector import connect

def dbconnect() -> object:
    return connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='books'
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

def get_all_books() -> list:
    sql = "SELECT * FROM bookinfo"
    return getprocess(sql)

def get_book_by_isbn(isbn: str) -> dict:
    # ISBN is treated as a string
    sql = "SELECT * FROM bookinfo WHERE isbn = %s"
    params = (isbn,)
    result = getprocess(sql, params)
    return result[0] if result else None

def add_book(isbn: str, title: str, author: str, copyright: str, edition: str, price: float, qty: int, total: float) -> bool:
    # ISBN is treated as a string
    sql = """
        INSERT INTO bookinfo (isbn, title, author, copyright, edition, price, qty, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (isbn, title, author, copyright, edition, price, qty, total)
    return postprocess(sql, params)

def get_book_by_id(book_id: int) -> dict:
    sql = "SELECT * FROM bookinfo WHERE id = %s"
    params = (book_id,)
    result = getprocess(sql, params)
    return result[0] if result else None

def update_book(book_id: int, isbn: str, title: str, author: str, copyright: str, edition: str, price: float, qty: int, total: float) -> bool:
    # ISBN is treated as a string
    sql = """
        UPDATE bookinfo
        SET isbn = %s, title = %s, author = %s, copyright = %s,
            edition = %s, price = %s, qty = %s, total = %s
        WHERE id = %s
    """
    params = (isbn, title, author, copyright, edition, price, qty, total, book_id)
    return postprocess(sql, params)

def delete_book(book_id: int) -> bool:
    sql = "DELETE FROM bookinfo WHERE id = %s"
    params = (book_id,)
    return postprocess(sql, params)
