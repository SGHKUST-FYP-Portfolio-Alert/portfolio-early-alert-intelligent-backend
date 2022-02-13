import numpy as np 
# import matplotlib.pyplot as plt

keywords = ["Ownership Change", "Change of Control", "Acceleration", "Accelerate", "Default", "Insolvency", "Insolvent", "Delay", "Late", "Failure", "Fail", "Dispute", "Liquidation", "Liquidator", "Margin call", "Haircut", "Bank Run", "Termination", "Moratorium", "Suspension", "Suspend", "Fraud", "Misrepresentation", "Fine", "Sanction", "Breach", "Reschedule", "Restructuring", "Restructure", "Credit Event", "Losses", "Loss", "Bailout", "Bailin", "Bankrupt", "Receivership", "Receiver", "Judicial Management", "Judicial Manager", "Administration", "Administrator", "Sequestrate", "Sequestration", "Support", "Capital call", "Liquidity Event", "Negative trends", "Price changes", "Board Infighting", "Corruption", "Inappropriate or ultra vires dealings", "Negative working capital", "Acquisition", "LBO", "Qualified audit opinion", "Regulatory Breach", "Non-performing Assets", "Provisions", "Force majeur", "Distress", "Frozen", "Delisted", "Sued", "Suit", "Arrested", "Disappeared", "Uncontactable"]

def keyword_count (news):
    
    keywords_count_dict = {}
    
    for keyword in keywords:
        keyword = keyword.lower()
        news = news.lower()
        if keyword in news:
            keywords_count_dict[keyword] = keywords_count_dict.get(keyword, 0) + 1
    
    return keywords_count_dict

