from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from database import database as db
from schemas.topic import Topic, TopicCreate
from typing import List
from ext_api.finnhub_wrapper import finnhub_client
from bson.objectid import ObjectId

router = APIRouter()

@router.get("", response_model=List[Topic])
def get_topics():
    result = []
    filter = { 'keywords': {"$exists": True} }
    for topic in db.get_topics(filter, projection={'embedding':False}):
        topic['id'] = str(topic['_id'])
        result.append(topic)
    print(topic)
    return result

@router.get("/", response_model=Topic)
def get_topic(id: str):
    id = ObjectId(id)
    result = db.get_topic(id=id)
    result['id'] = str(result['_id'])
    return result

@router.post("", status_code=201)
def add_topic(topic: TopicCreate):
    topic = jsonable_encoder(topic)
    db.add_topic(topic)

@router.put("")
def update_topic(topic: Topic):
    topic = jsonable_encoder(topic)
    topic['_id'] = ObjectId(topic['id'])
    del topic['id']
    db.update_topic(topic)


@router.delete("")
def delete_topic(id: str):
    id = ObjectId(id)
    db.delete_topic(id)