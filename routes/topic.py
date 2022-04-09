import logging
import numpy as np

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from calculations.topicScorer import scorer
from database import database as db
from schemas.topic import Topic, TopicCreate
from typing import List
from ext_api.finnhub_wrapper import finnhub_client
from bson.objectid import ObjectId

router = APIRouter()
logger = logging.getLogger(__name__)

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

def gen_topic_embed(topic: TopicCreate):
    # regex: \b(keyword1)\b|\b(keyword2)\b/i
    regex = [f'\\b({x})\\b' for x in topic['keywords']]
    regex = '|'.join(regex)

    # get all news embedding with keywords in headline
    cur = db.get_news({'headline': { '$regex': regex, '$options' : 'i' },
                        'embedding': { '$exists': True } }, 
                        projection={'_id':1, 'headline':1, 'embedding':1})

    embedding = [news['embedding'] for news in list(cur)]
    
    if len(embedding) <= 1:
        logger.warning(f'Topic {topic["title"]} has less than 2 news matches')
        return False

    topic['embedding'] = np.mean(np.array(embedding), axis=0).tolist()

    return topic

@router.post("", status_code=201)
def add_topic(topic: TopicCreate):
    topic = jsonable_encoder(topic)
    topic = gen_topic_embed(topic)
    if topic:
        scorer.add_topic(topic)
    else:
        raise HTTPException(status_code=400, detail='Topic embedding not generated')

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