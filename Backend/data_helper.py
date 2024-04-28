import mysql.connector
global db_connection

db_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "pandeyji_eatery"
)

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = db_connection.cursor()
        
        #calling the stored procedure
        cursor.callproc("insert_order_item", (food_item, quantity, order_id))
        
        #commit the transaction
        db_connection.commit()
        
        cursor.close()
        
        print("Order item inserted successfully!")
        
        return 1
        
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        
        #rollback chanegs in case of error()
        db_connection.rollback()
        
        return -1

    except Exception as e:
        print(f"Error inserting order item: {e}")        
        #rollback chanegs in case of error
        db_connection.rollback()
        
        return -1
    
    
    
def insert_order_tracking(order_id, status):
    cursor = db_connection.cursor()
    
    #inserting the record in the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    
    #commit the changes
    db_connection.commit()
    
    cursor.close()



def next_order_id():
    cursor = db_connection.cursor()
    
    #executing the SQL query to get the next order id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    
    #fetching the result
    result = cursor.fetchone()[0]
    
    cursor.close()
    
    if result is None:
        return 1
    else : 
        return result + 1
    
    
def get_order_status(order_id : int):
    
    #create a cursor object
    cursor = db_connection.cursor()
    
    #sql query
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    
    #execute the query
    cursor.execute(query, (order_id,))
    
    #fetch the result
    result = cursor.fetchone()
    
    cursor.close()
    
    if result is not None:
        return result[0]
    else:
        return None
    
def get_order_total(order_id : int):
    cursor = db_connection.cursor()
    
    query = f"SELECT get_total_order_price({order_id})"
    
    cursor.execute(query)
    
    result = cursor.fetchone()[0]
    
    cursor.close()
    
    return result