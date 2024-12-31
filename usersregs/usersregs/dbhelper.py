'''
	database helper
'''
from mysql.connector import connect

def dbconnect()->object:
    return connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='myuser'
    )
    
def getprocess(sql:str)->list:
    db:object = dbconnect()
    cursor:object = db.cursor(dictionary=True)
    cursor.execute(sql)
    data:list = cursor.fetchall()
    cursor.close()
    return data
    
    
def postprocess(sql:str)->bool:
    db:object = dbconnect()
    cursor:object = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    return True if cursor.rowcount>0 else False
    

def getall_record(table:str)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql)
    
    
def addnewuser(name:str,username:str,password:str)->bool:
    sql:str = f"INSERT INTO `users`(`name`,`username`,`password`) VALUES('{name}','{username}','{password}')"
    print(sql)
    return postprocess(sql)
    
    

def validateuser(username:str,password:str)->list:
    sql:str = f"SELECT * FROM `users` WHERE `username`= '{username}' AND `password`='{password}'"
    return getprocess(sql)
    
