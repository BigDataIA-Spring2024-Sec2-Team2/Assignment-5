from datetime import datetime
from bson.objectid import ObjectId
from fastapi import APIRouter, Header, status, HTTPException
from pymongo import MongoClient
import configparser
import jwt
from pydantic import BaseModel

router = APIRouter()

config = configparser.ConfigParser()
config.read('configuration.properties')

# JWT config
SECRET_KEY = config['auth-api']['SECRET_KEY']
ALGORITHM = config['auth-api']['ALGORITHM']

# mongo config
mongo_url = config['MongoDB']['mongo_url']
db_name = config['MongoDB']['db_name']
collection_name_data = config['MongoDB']['collection_name_data']
collection_name_markdown = config['MongoDB']['collection_name_markdown']


@router.get('/topics')
async def get_topic_list( authorization: str = Header(None)):
    ''' get loaded topic list '''
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM, ])
        email: str = token_decode.get("sub")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token has expired")
    # create client
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[collection_name_data]
    query = {"Status": True}
    cursor = collection.find(query)
    records = [ i["NameOfTheTopic"] for i in cursor]
    client.close()
    return {"topics": records}

class markdownTopic(BaseModel):
    topic: str

@router.get('/markdown')
async def get_markdown( payload: markdownTopic, authorization: str = Header(None)):
    ''' get markdown for topic '''
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = parts[1]
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM, ])
        email: str = token_decode.get("sub")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token has expired")
    # create client
    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[collection_name_markdown]
    query = {"NameOfTheTopic": payload.topic}
    cursor = collection.find(query)
    learning_map = {}
    for i in cursor:
        learning_map[i["Learning"]] = i["LearningSummary"]
    client.close()
    return {"markdown": learning_map}