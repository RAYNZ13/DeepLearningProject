import mysql.connector

db_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "pandeyji_eatery"
)

def get_order_status(order_id : int):
    #create  a connection to the database

    
    #create a cursor object
    cursor = db_connection.cursor()
    
    #sql query
    query = ("SELECT status FROM order_tracking WHERE order_id = %s")
    
    #execute the query
    cursor.execute(query, (order_id,))
    
    #fetch the result
    result = cursor.fetchone()
    
    if result is not None:
        return result[0]
    else:
        return None