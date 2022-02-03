from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 

nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words('english')

def sents_to_words(sentences):
    for sentence in sentences:
        yield(simple_preprocess(str(sentence), deacc=True))
        
def remove_stopwords(docs):
    refined_docs = []
    
    for doc in docs:
        refined_doc = []
        for word in simple_preprocess(str(doc)):
            if word not in stop_words and len(word) > 4:
                refined_doc.append(word)
        refined_docs.append(refined_doc)
        
    return refined_docs

def get_lda(sentences, num_topics):
    docs = list(sents_to_words(sentences))
    docs = remove_stopwords(docs)
    id2word = corpora.Dictionary(docs)
    corpus = [id2word.doc2bow(doc) for doc in docs]

    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                        id2word=id2word,
                                       num_topics=num_topics)
    return lda_model