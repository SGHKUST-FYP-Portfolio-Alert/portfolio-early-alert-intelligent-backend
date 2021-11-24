# brainstorming how to determine relationship of words with the sentiment

'''
call the finbert model to get the sentiment
for each retrieved sentiment (especially the ones that are very high and low towards the spectrum) for a news segment:
    go through the news and find out the main keywords:
        call the heatmap from keywordModelling.py to get a view

Researched LDA: Does not seem much reliable.
'''
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import random

#openning the file using pandas
npr = pd.read_csv('file:..\\\data\\npr.csv')

#initializing the count vectorizer
#max document frequencey means that the percentage of max frequency shuld be less than 90% of any word across documents
#min document frequencey is an integer, means that a word must occur at least 2 or more times to be counted
#stop words will be automatically tackled through sklearn 
cv = CountVectorizer(max_df=0.9, min_df=2, stop_words='english')

#the fit transform method will return a sparse matrix (numberofariticles x totalwords)
dtm  = cv.fit_transform(npr['Article'])

#initialize the LDA, n_components =7 means that we are opting for 7 distinct topics
#the n_components depends upon how big is the repository and how many topics you want to discover
#keep the random state as 42
LDA = LatentDirichletAllocation(n_components=7, random_state=42)

#fit the model into lda
LDA.fit(dtm)

#grab the vocabulary of words
#get the random words 
random_int = random.randint(0,54777)

cv.get_feature_names()[random_int] #this function will get the words from the document

#grab the topics
single_topic = LDA.components_[0]


#this way we can get index position for high probablity topics SORTED by probablity in ASC order
top_10_words = single_topic.argsort()[-10:] #to get the last 10 highest probablity words for this topic


for index in top_10_words:
    print(cv.get_feature_names()[index])
    
#grab the highest probablity words per topic
for i, topic in enumerate(LDA.components_):
    print(f"The top 15 words for the topic #{i}")
    print([cv.get_feature_names()[index] for index in topic.argsort()[-10:]]) 
    print("\n")
    print("\n")


#attach the topic number to the original topics
topic_results = LDA.transform(dtm)

topic_results[0]
 
    
print("finished..")