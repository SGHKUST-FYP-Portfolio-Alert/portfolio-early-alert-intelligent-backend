import asyncio
from database import database as db
from pytorch_pretrained_bert import BertTokenizer
from models.bertModel import BertClassification
from datetime import timezone
import datetime
import torch
import torch.nn.functional as F

def main():
    labels = {0:'neutral', 1:'positive',2:'negative'}
    num_labels= len(labels)
    vocab = "finance-uncased"
    vocab_path = 'analyst_tone/vocab'
    pretrained_weights_path = "analyst_tone/pretrained_weights" # this is pre-trained FinBERT weights
    fine_tuned_weight_path = "analyst_tone/fine_tuned.pth"      # this is fine-tuned FinBERT weights
    max_seq_length=512
    device='cpu'
    model = BertClassification(weight_path= pretrained_weights_path, num_labels=num_labels, vocab=vocab)
    model.load_state_dict(torch.load(fine_tuned_weight_path, map_location='cpu'))
    model.to(device)
    start_dt = datetime.datetime(2021, 10, 1)
    unix_start_dt = start_dt.replace(tzinfo=timezone.utc).timestamp()
    end_dt = datetime.datetime(2021, 10, 16)
    unix_end_dt = end_dt.replace(tzinfo=timezone.utc).timestamp()
    news = db.get_news({"datetime":{"$gte":unix_start_dt,"$lt":unix_end_dt}, "counterparty": "AAPL", "source": "Yahoo"})
    id_loop = [data['id'] for data in news]
    sentences = [data['headline'] for data in news]
    tokenizer = BertTokenizer(vocab_file = vocab_path, do_lower_case = True, do_basic_tokenize = True)
    model.eval()
    result_list = []
    for id, sent in zip(id_loop,sentences): 
        tokenized_sent = tokenizer.tokenize(sent)
        if len(tokenized_sent) > max_seq_length:
            tokenized_sent = tokenized_sent[:max_seq_length]
        
        ids_review  = tokenizer.convert_tokens_to_ids(tokenized_sent)
        mask_input = [1]*len(ids_review)        
        padding = [0] * (max_seq_length - len(ids_review))
        ids_review += padding
        mask_input += padding
        input_type = [0]*max_seq_length
        
        input_ids = torch.tensor(ids_review).to(device).reshape(-1, max_seq_length)
        attention_mask =  torch.tensor(mask_input).to(device).reshape(-1, max_seq_length)
        token_type_ids = torch.tensor(input_type).to(device).reshape(-1, max_seq_length)
        with torch.set_grad_enabled(False):
            outputs = model(input_ids, token_type_ids, attention_mask)
            outputs = F.softmax(outputs,dim=1)
            sentiment_score = 0
            if labels[torch.argmax(outputs).item()]=="positive":
                sentiment_score = 1
            elif labels[torch.argmax(outputs).item()]=="neutral":
                sentiment_score = 0
            elif labels[torch.argmax(outputs).item()]=="negative":
                sentiment_score = -1
            result_list.append({"id":id, "sentiment":sentiment_score})
    db.update_news(result_list)
if __name__ == '__main__':
    main()