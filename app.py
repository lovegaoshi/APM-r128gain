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


# Data model


class ItemCreate(BaseModel):
    itemid: str
    r128gain: str | None = None
    abrepeat: str | None = None


@app.get('/')
async def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000)
