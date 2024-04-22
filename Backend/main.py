from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):

    payload = await request.json()
    
    intent = payload.get("queryResult").get("intent").get("displayName")
    parameters = payload.get("queryResult").get("parameters")
    output_contexts = payload.get("queryResult").get("outputContexts")
    
    if intent == "track order - context: ongoing-tracking":
        return JSONResponse(content=
            {"fulfillmentText": f"Received =={intent}== in the backend"})
        
        