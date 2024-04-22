from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

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
        return JSONResponse(content=
            {"fulfillmentText": f"Received =={intent}== in the backend"})
    
def    
        