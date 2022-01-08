from pymongo import UpdateOne

def InsertIfNotExist(document):
    return UpdateOne(
        document, 
        {'$setOnInsert': document},
        upsert=True
    )