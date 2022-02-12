from database import database as db

def weighted_rolling_average(avgs: list, weights: list, decay=0.8):

    r_avgs = []
    r_weights = []

    for avg, weight in zip(avgs, weights):
        if len(r_avgs) == 0:
            prev_r_weight = 0
            prev_r_avg = 0
        else:
            prev_r_weight = r_weights[-1]
            prev_r_avg = r_avgs[-1]
        
        r_weight = decay * prev_r_weight + weight
        r_avg = (decay * prev_r_weight * prev_r_avg + avg * weight)/(r_weight or 1)

        r_avgs.append(r_avg)
        r_weights.append(r_weight)

    return (r_avgs, r_weights)

def aggregate_sentiments_daily():
    
    pipeline = [
        {'$group': {'_id': { 'date': '$date', 'counterparty': '$counterparty', 'sentiment': '$sentiment'}, 'count':{'$sum':1}}},
        {'$group': {'_id': {'date':'$_id.date', 'counterparty':'$_id.counterparty'}, 'news_count': {'$sum': '$count'}, 'sentiments': {'$addToSet' : {'k': {'$toString': '$_id.sentiment'}, 'v':'$count'}}}},
        {'$project': {'_id': 0, 'date':'$_id.date', 'counterparty':'$_id.counterparty', 'news_count': 1, 'sentiments': {'$arrayToObject': '$sentiments'} }},
        {'$group': {'_id': '$counterparty', 'results': {'$push': {'date': '$date', 'news_count': '$news_count', 'sentiments': '$sentiments'}}}},
        {'$project':{'_id': 0, 'counterparty': '$_id', 'results': 1}}
    ]

    aggregated = db.aggregate_news(pipeline)

    output = []
    for a in aggregated:
        results = sorted(a['results'], key= lambda x: x['date'])
        weights = [
            r['sentiments'].get('1', 0) + r['sentiments'].get('-1', 0) + 0.25 * r['sentiments'].get('0', 0)
        for r in results]
        avgs = [
            (r['sentiments'].get('1', 0) - r['sentiments'].get('-1', 0))/w
        for r, w in zip(results, weights)]
        r_avgs, r_weights = weighted_rolling_average(avgs, weights)
        for r, r_avg, r_weight in zip(results, r_avgs, r_weights):
            r['sentiments']['rolling_avg'] = r_avg
            r['sentiments']['rolling_weight'] = r_weight
            r['counterparty'] = a['counterparty']
            output.append(r)

    return output




def aggregate_keywords_news_count_daily():

    pipeline =  [
        {'$group': {'_id': {'date': '$date', 'counterparty':'$counterparty'}, 'keyword_count': {'$mergeObjects': '$keyword_count'}, 'news_count': {'$sum':1}}},
        {'$project': {'_id': 0, 'date':'$_id.date', 'counterparty':'$_id.counterparty', 'keyword_count': 1, 'news_count': 1}}
    ]

    return db.aggregate_news(pipeline)
