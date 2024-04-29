from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import data_helper
import generic_helper

app = FastAPI()

#a new dictionary to store the order details
inprogress_orders = {
    
}

@app.post("/")
async def handle_request(request: Request):
    #retrive the JSON data from the request
    payload = await request.json()
    
    # Extract the necessary information from the payload
    # based on the structure of the WebHookReq from DialogFlow
    intent = payload.get("queryResult").get("intent").get("displayName")
    parameters = payload.get("queryResult").get("parameters")
    output_contexts = payload.get("queryResult").get("outputContexts")
    
    session_ID = generic_helper.extract_sessionID(output_contexts[0]['name'])
    
    #create a dictionary as a routing table for the intents with the functions to avoid the ugly if else
    intent_handler_dict = {
        #intent : fucntion
        'Order.add - context: ongoing-order' : add_to_order,
        'order.remove - context: ongoing-order' : remove_from_order,
        'order.complete - context: ongoing-order' : complete_order,
        'track order - context: ongoing-tracking' : track_order
    }
    
    return intent_handler_dict[intent](parameters, session_ID)

def remove_from_order(parameter : dict, session_ID : str):
    if session_ID not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText" : "I'm having a trouble finding your order. Sorry! Can you please place a order once again ?"
        })
    else :
        current_order =  inprogress_orders[session_ID]
        food_items = parameter["food-items"]
        
        #to keep track of the removed item and the items that are not found
        removed_items = []
        no_such_items = []
        
        #to remove item
        for item in food_items:
            if item not in current_order:
                no_such_items.append(item)
            else : 
                removed_items.append(item)
                del current_order[item]
        if len(removed_items) > 0 :
            fulfillment_text = f'Removed {",".join(removed_items)} from your order'
        
        if len(no_such_items) > 0:
            fulfillment_text = f'Your current order does not have {",".join(no_such_items)}'

        if len(current_order.keys()) == 0:
            fulfillment_text += "Your order is empty!"
        else:
            current_order_str = generic_helper.get_str_from_food_dict(current_order)
            fulfillment_text += f"Here's what is left in yout order: {current_order_str}"
            
        return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })
#add to order function
def add_to_order(parameters : dict, session_ID : str):
    food_item = parameters["food-items"]
    quantity = parameters["number"]
    
    if len(food_item) != len(quantity):
        fulfillment_text = "Sorry I didn't understand the order. Can you please specify the food items and qunatity again?"
    else:
        news_food_dict = dict(zip(food_item, quantity))
        
        if session_ID in inprogress_orders:
            current_food_dict = inprogress_orders[session_ID]
            current_food_dict.update(news_food_dict)
            inprogress_orders[session_ID] = current_food_dict    
        else:
            inprogress_orders[session_ID] = news_food_dict
            
        # print("*****************************************")
        # print(session_ID)
        # print(inprogress_orders[session_ID])
        
        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_ID])
        fulfillment_text = f"So far you have: {order_str} . D you want to add anything else?"
        
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
      
      
def complete_order(parameters: dict, session_ID: str):
    if session_ID not in inprogress_orders:
        fulfillment_text = "Sorry, I could not find any order in progress. Can you please place a new order again?"
    else:
        order = inprogress_orders[session_ID]
        order_id = save_to_database(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I could not place the order. Can you please try again?"
        else:
            order_total = data_helper.get_order_total(order_id)
            if order_total is None:
                fulfillment_text = "Sorry, there was an issue calculating the order total. Please try again later."
            else:
                fulfillment_text = f"Order placed successfully. Your order id is {order_id}. You can track your order using this order id.  Your order total is {order_total} which you can pay at the time of delivery." \
                                   f"Hurray, we have place your order. Here is your order id {order_id}. You can track your order using this order id. Your order total is {order_total}"\
                                   f"Your order is on the way. You can track your order using this order id {order_id}, Your order total is {order_total} which you can pay at the time of delivery." 

        del inprogress_orders[session_ID]  # Remove the order from inprogress_orders once placed

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

        
        
def save_to_database(order : dict):
    #order = {"pizza": 2, "chole": 1}
    next_order_id = data_helper.next_order_id()
    for food_item, quantity in order.items():
        rcode = data_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )
    
        if rcode == -1:
            return -1
        
    data_helper.insert_order_tracking(next_order_id, "in progress")
    return  next_order_id

    
    
    # if intent == "track order - context: ongoing-tracking":
    #     return track_order(parameters)
    #     # return JSONResponse(content={
    #     #     "fulfillmentText":f"Recieved =={intent}== in the backend"
    #     # })
       
       

    
def track_order(parameters : dict, session_ID: str):
    order_id = int(parameters['number'])
    order_status = data_helper.get_order_status(order_id)
    
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is {order_status}"
    else :
        fulfillment_text = f"Sorry, No order found with order id: {order_id}"
        
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
    
        