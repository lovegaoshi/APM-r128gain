from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging
import os

app = FastAPI(docs_url=os.environ['DOCS_PATH'])

# MongoDB configuration
MONGO_URL = os.environ['MONGO_PATH']
DATABASE_NAME = "APM"
COLLECTION_NAME = "r128gain"
UPLOAD_PATH = os.environ['ADD_PATH']
GETALL_PATH = os.environ['GET_PATH']


@app.post(UPLOAD_PATH, status_code=200)
async def create_item(itemid: str, r128gain: str | None = None, abrepeat: str | None = None):
    # MongoDB client setup
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    new_item = {"itemid": itemid}
    if r128gain is not None:
        new_item["r128gain"] = r128gain
    if abrepeat is not None:
        new_item["abrepeat"] = abrepeat
    try:
        await collection.update_one({"itemid": itemid}, {"$set": new_item}, upsert=True)
        return 'oK'
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="oh noe.")


@app.get(GETALL_PATH)
async def get_all() -> JSONResponse:
    # MongoDB client setup
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    item = await collection.find({}, {"_id": False}).to_list(length=None)
    if item:
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)

    raise HTTPException(status_code=404, detail="Item not found")


@app.get('/')
async def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000)
