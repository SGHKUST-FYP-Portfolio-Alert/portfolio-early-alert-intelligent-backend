'''
pass news headline, summary and company name/symbol
things to be researched: LDA (Latent Dirichlet Allocation)
'''

import numpy as np 
# import matplotlib.pyplot as plt

keywords = ["Ownership change", "Change of control", "Acceleration", "accelerate", "Default", "Insolvency", "Insolvent", "Delay", "Late", "Failure", "fail", "Dispute", "Liquidation", "Liquidator", "Margin call", "Haircut", "Bank run", "Termination", "Moratorium", "Suspension", "Suspend", "Fraud", "misrepresentation", "Fine", "sanction", "Breach", "Reschedule", "Restructuring", "Restructure", "Credit event", "Losses", "Loss", "Bailout", "Bailin", "Bankrupt", "Receivership", "Receiver", "Judicial Management", "Judicial Manager", "Administration", "Administrator", "Sequestrate", "Sequestration", "Support", "Capital call", "Liquidity event", "Negative trends", "Price changes", "Board infighting", "Corruption", "Inappropriate or ultra vires dealings", "Negative working capital", "Acquisition", "LBO", "Qualified audit opinion", "Regulatory breach", "Non-performing assets", "Provisions", "Force majeur", "Distress", "Frozen", "Delisted", "Sued", "Suit", "Arrested", "Disappeared", "Uncontactable"]

def keyword_count (news: str, keywords: str = keywords):

    keyword_count_dict = {}

    for keyword in keywords:
        count = news.count(keyword)
        if count:
            keyword_count_dict[keyword] = count
    
    return keyword_count_dict

# def key_word_heatmap (keywords, keyword_count_dict):

#     keywords_count = np.array([keyword_count_dict.values()])

#     fig, ax = plt.subplots()
#     im = ax.imshow(keywords_count)

#     # We want to show all ticks...
#     ax.set_yticks(np.arange(len(keywords)))
#     ax.set_yticklabels(keywords)

#     # Rotate the tick labels and set their alignment.
#     plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#             rotation_mode="anchor")

#     # Loop over data dimensions and create text annotations.
#     for i in range(len(keywords)):
#         for j in range(len(keywords)):
#             text = ax.text(j, i, keywords_count[i, j],
#                         ha="center", va="center", color="w")

#     ax.set_title("Keyword vs Keyword Count")
#     fig.tight_layout()
#     plt.show()




