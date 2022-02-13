from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
import torch

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3).to(device)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

