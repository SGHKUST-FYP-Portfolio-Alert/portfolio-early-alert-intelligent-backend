from typing import List

from sklearn.metrics.pairwise import cosine_similarity

from database import database as db
from schemas.topic import TopicCreate

class topicScorer:
    def __init__(self):
        self.titles = []
        self.embeddings = []

        # fill in the embeddings and titles from db
        filter = { 'embedding': {"$exists": True} }
        entries = { '_id': 0, 'title': 1, 'embedding': 1 }
        for entry in list(db.get_topics(filter=filter, projection=entries)):
            self.titles.append(entry['title'])
            self.embeddings.append(entry['embedding'])

    '''
    Parameters:
        embedding (np.array): (number of sentences, max_token_len*768)

    Returns:
        topic_scores (list): [{topic 1: score, ...} * number of sentences]
    '''
    def score(self, embeddings) -> List[dict]:
        #(number of sentences, number of topics)
        score_mat = cosine_similarity(embeddings, self.embeddings)

        result = []
        for i in range(len(embeddings)):
            result.append(dict(zip(self.titles, score_mat[i])))

        return result

    def add_topic(self, topic: TopicCreate):
        self.titles.append(topic['title'])
        self.embeddings.append(topic['embedding'])

        db.add_topic(topic)

scorer = topicScorer()
