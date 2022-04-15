print('begin')

# keywords = ["Ownership Change", "Change of Control", "Acceleration", "Accelerate", "Default", "Insolvency", "Insolvent", "Delay", \
#         "Late", "Failure", "Fail", "Dispute", "Liquidation", "Liquidator", "Margin call", "Haircut", "Bank Run", "Termination", "Moratorium", \
#         "Suspension", "Suspend", "Fraud", "Misrepresentation", "Fine", "Sanction", "Breach", "Reschedule", "Restructuring", "Restructure", \
#         "Credit Event", "Losses", "Loss", "Bailout", "Bailing", "Bankrupt", "Receivership", "Receiver", "Judicial Management", "Judicial Manager", \
#         "Administration", "Administrator", "Sequestrate", "Sequestration", "Support", "Capital call", "Liquidity Event", "Negative trends", \
#         "Price changes", "Board Infighting", "Corruption", "Inappropriate or ultra vires dealings", "Negative working capital", "Acquisition", \
#         "LBO", "Qualified audit opinion", "Regulatory Breach", "Non-performing Assets", "Provisions", "Force majeure", "Distress", "Frozen", \
#         "Delisted", "Sued", "Suit", "Arrested", "Disappeared", "Uncontactable"]

topics = {"Admin Change": ["Administration", "Administrator", "Ownership", "Change of Control", "Restructuring", "Restructure", "Board", "Corruption", "Acquisition"], "Ups & Downs": ["Acceleration", "Accelerate", "Deceleration", "Deceleration", "Price"], "Ups": ["Acceleration", "Accelerate"], "Downs": ["Deceleration", "Deceleration"], "Default": ["Default", "Delay", "Late", "Failure", "Fail", "Suspension", "Suspend", "Termination", "Fraud", "Dispute", "Moratorium", "Bankrupt", "Insolvency",  "Insolvent", "Liquidation", "Liquidator"], "Seizing": ["Bank Run", "Receivership", "Receiver", "Judicial", "Sequestrate", "Sequestration", "LBO", "audit", "Provisions"], "Loss": ["Misrepresentation", "Fine", "Sanction", "Breach", "Reschedule", "Losses", "Loss", "Credit Event", "Bailout", "bailing", "Margin calls", "Haircut", "Support", "Negative",  "Non-performing Assets"], "Law Suits": ["Force majeure", "Distress", "Frozen", "Delisted", "Sued", "Suit", "Arrested", "Disappeared"]}

# keywords = ['ownership', 'margin calls', 'bailing', 'judicial', 'capital', 'liquidity', 'price', 'negative', 'board', 'audit', 'regulatory'] #better keywords to replace the crap ones

import requests

for key in topics:
    resp = requests.post('http://localhost:8080/topic', json = {'title': f'{key}', 'keywords': topics[key], 'counterparties': 'global'})
    print('-', key, resp, resp.content)