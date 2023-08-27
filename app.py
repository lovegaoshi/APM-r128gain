from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import logging
import os

app = FastAPI(docs_url=os.environ['DOCS_PATH'])

# MongoDB configuration
MONGO_URL = os.environ['MONGO_PATH']
DATABASE_NAME = "APM"
COLLECTION_NAME = "r128gain"


# MongoDB client setup
client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
ADD_PATH = os.environ['ADD_PATH']
GET_PATH = os.environ['GET_PATH']

# Data model


class ItemCreate(BaseModel):
    itemid: str
    r128gain: str | None = None
    abrepeat: str | None = None

# Routes


@app.post(ADD_PATH, status_code=200)
async def create_item(item: ItemCreate) -> None:
    new_item = {"itemid": item.itemid}
    if item.r128gain is not None:
        new_item["r128gain"] = item.r128gain
    if item.abrepeat is not None:
        new_item["abrepeat"] = item.abrepeat
    try:
        await collection.update_one({"itemid": item.itemid}, {"$set": new_item}, upsert=True)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail="oh noe.")


@app.get(GET_PATH)
async def get_all() -> JSONResponse:
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
