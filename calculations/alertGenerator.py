import pandas as pd
from datetime import timedelta

class alertGenerator:
    
    def __init__(self):
        self.percentile_cutoff = 0.05
        pass

    def generate_sentiment_alert(self, dates: list, scores: list):
        df = pd.DataFrame(zip(dates, scores), columns=['date', 'score'])
        df['date'] = pd.to_datetime(df.index)
        
        df['d_score'] = df['score'].pct_change()
        df.dropna(inplace=True)
        df['percentile'] = df['d_score'].rank(pct=True)

        low_percentiles = df[df['percentile'] < self.percentile_cutoff]
        high_percentiles = df[df['percentile'] > 1-self.percentile_cutoff]

        for _, row in low_percentiles.iterrows():
            db.add_alert({
                'date': row['date'],
                'class': 'alert',
                'type': 'sentiment drop',
                'value': row['d_score'],
                'percentile': row['cdf']
            })
        
        for _, row in high_percentiles.iterrows():
            db.add_alert({
                'date': row['date'],
                'class': 'reminder',
                'type': 'sentiment raise',
                'value': row['d_score'],
                'percentile': 1 - row['cdf']
            })



