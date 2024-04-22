from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
# import dataBaseHelper

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    #retrive the json data from the request
    payload = await request.json()
    
    #extract the necessary info from payload
    #based on the structre pf the webhookrequest from dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    
    if intent == 'track order - context: ongoing-tracking':
        # return track_order(parameters,intent)
        return JSONResponse(content={
            "fulfillmentText":f"Recieved =={intent}== in the backend"
        })
        
        
        

        
# def track_order(parameters: dict,intent: str):
#     order_id = parameters['order_id']
#     order_status = dataBaseHelper.read_order_status(order_id)
#     if order_status:
#         fulfilllemt_text = f"The order staus for the order id {order_id} is : {order_status}"
#     else : 
#         fulfilllemt_text = f"No order found for the order id {order_id}"   
#     return JSONResponse(
#         content = {"fulfillmentText":f"Recieved =={intent}== in the backend"}
#     )