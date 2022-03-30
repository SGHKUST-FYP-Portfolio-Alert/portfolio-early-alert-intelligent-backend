import pandas as pd
from datetime import timedelta
from database import database as db

class AlertGenerator:
    
    def __init__(self):
        self.percentile_cutoff = 0.05
        pass

    def generate_sentiment_alert(self, counterparty, dates: list, scores: list):
        df = pd.DataFrame(zip(dates, scores), columns=['date', 'score'])
        df['date'] = pd.to_datetime(df['date'])
        
        df['d_score1'] = df['score'].diff()
        df['d_score2'] = df['score'].diff(periods=2)
        df['d_score3'] = df['score'].diff(periods=3)
        df['d_score'] = df[['d_score1', 'd_score2', 'd_score3']].mean(axis=1)
        df.dropna(inplace=True)
        df['percentile'] = df['d_score'].rank(pct=True)

        low_percentiles = df[df['percentile'] < self.percentile_cutoff]
        high_percentiles = df[df['percentile'] > 1-self.percentile_cutoff]

        for _, row in low_percentiles.iterrows():
            db.add_alert({
                'date': row['date'],
                'class': 'alert',
                'counterparty': counterparty,
                'type': 'sentiment drop',
                'value': row['d_score'],
                'percentile': row['percentile']
            })
        
        for _, row in high_percentiles.iterrows():
            db.add_alert({
                'date': row['date'],
                'class': 'reminder',
                'counterparty': counterparty,
                'type': 'sentiment raise',
                'value': row['d_score'],
                'percentile': 1 - row['percentile']
            })



alertGenerator = AlertGenerator()