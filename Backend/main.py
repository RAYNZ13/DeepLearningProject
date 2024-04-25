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
        # 'order.remove - context: ongoing-order' : remove_from_order,
        # 'order.complete - context: ongoing-order' : complete_order,
        'track order - context: ongoing-tracking' : track_order
    }
    
    return intent_handler_dict[intent](parameters, session_ID)



#add to order function
def add_to_order(parameters : dict):
    food_item = parameters["food-items"]
    quantity = parameters["number"]
    
    if len(food_item) != len(quantity):
        fulfillment_text = "Sorry I didn't understand the order. Can you please specify the food items and qunatity again?"
    else:
        fulfillment_text = f"Recived {food_item} and {quantity} in the backend"
        
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
        
    
    # if intent == "track order - context: ongoing-tracking":
    #     return track_order(parameters)
    #     # return JSONResponse(content={
    #     #     "fulfillmentText":f"Recieved =={intent}== in the backend"
    #     # })
       
    
def track_order(parameters : dict):
    order_id = int(parameters['number'])
    order_status = data_helper.get_order_status(order_id)
    
    if order_status:
        fulfillment_Text = f"The order status for order id: {order_id} is {order_status}"
    else :
        fulfillment_Text = f"Sorry, we could not find any order with order id: {order_id}"
        
    return JSONResponse(content={
        "fulfillmentText": fulfillment_Text
    })
    
        