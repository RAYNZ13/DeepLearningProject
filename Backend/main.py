from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import data_helper

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    #retrive the JSON data from the request
    payload = await request.json()
    
    # Extract the necessary information from the payload
    # based on the structure of the WebHookReq from DialogFlow
    intent = payload.get("queryResult").get("intent").get("displayName")
    parameters = payload.get("queryResult").get("parameters")
    output_contexts = payload.get("queryResult").get("outputContexts")
    
    if intent == "track order - context: ongoing-tracking":
        return track_order(parameters)
        # return JSONResponse(content={
        #     "fulfillmentText":f"Recieved =={intent}== in the backend"
        # })
        
    
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
    
        