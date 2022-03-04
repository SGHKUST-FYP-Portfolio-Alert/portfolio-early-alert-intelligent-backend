# from pytorch_pretrained_bert import BertTokenizer
# from pytorch_pretrained_bert.tokenization import VOCAB_NAME
# from models.bertModel import BertClassification
from typing import List
# import torch
# from typing import List
# import time
# import torch.nn.functional as F

import numpy as np
import utils

from transformers import BertTokenizer, BertForSequenceClassification

class transformerInfer:
    def __init__(self, config, news: List[dict] = None):
        self.news = news if news != None else []

        self.labels = config.labels
        self.max_len = config.max_seq_length
        self.batch_size = config.batch_size
        self.device = config.device

        self.class2sent_map = {0: 0, 1: 1, 2: -1}

        self.tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        self.model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3).to(self.device)
    
    def set_news(self, news: List[dict]):
        self.news = news

    def __tokenize(self, sentences):
        return self.tokenizer(sentences, return_tensors="pt", max_length=self.max_len , padding='max_length', truncation=True).to(self.device)

    '''returns: list of dicts, each dict contains _id and sentiment (from -1 to 1)'''
    def infer(self):
        result_list = []

        #inference loop, processing batch_size sentences at a time
        for news in utils.chunks(self.news, self.batch_size):
            sentences = [data['headline'] for data in news]
            
            inputs = self.__tokenize(sentences)
            outputs = self.model(**inputs, output_hidden_states=True)

            # 1d array of batch_size, each classified from 0 to 2
            classifications = np.argmax(outputs[0].detach().numpy(), axis=1)
            self.classifications = classifications

            result_list += [{'_id': data['_id'], 'sentiment': self.class2sent_map[classifications[i]]} for i, data in enumerate(news)]
        
        return result_list
        #TODO: document func, ram usage, review all changes
