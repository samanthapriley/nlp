# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following is a basic script to make barplot representations of top pos in seaborn

Required inputs:
    -product of the top_pos script (dataframe with top pos/coca index)
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import numpy as np

# DATA #
import pandas as pd
df = pd.DataFrame(pd.read_csv(r'C:\Users\samantha.riley\Desktop\requests1.csv'), columns=['Topic', 'requests', 'Rate'])
print(df)
# with open(r"C:\\Users\\samantha.riley\\PycharmProjects\\Farxiga\\Final Deck\\pos\\pos.pickle", 'rb') as handle:
#     df = pickle.load(handle)

adj = df.loc[df['pos'] == 'adj']
# noun = df.loc[df['pos'] == 'noun']
# verb = df.loc[df['pos'] == 'verb']

# PLOT #
# Optional- custom palette based on coca index value
# custom_palette = {}
# for word in set(adj.Word):
#     ix = (np.sum(adj.loc[adj.Word == word].Index))
#     if ix > 500:
#         custom_palette[word] = 'r'
#     elif ix > 1000:
#         custom_palette[word] = 'y'
#     else:
#         custom_palette[word] = 'g'

adj = sns.barplot(x=df['Topic'], y=df['Rate'], palette="Purples_r")
ax = plt.gca().axes
ax.get_yaxis().set_visible(False)
ax.set_xlabel('')
sns.despine(top=True, right=True, left=True)
adj.set_xticklabels(adj.get_xticklabels(), rotation=50, ha='right')
plt.title('Topic Requests')
plt.tight_layout()
for index, row in df.iterrows():
    adj.text(row.name,row.Rate + 0.002, "{}%".format(round(row.Rate,2) * 100), color='black', ha="center")
plt.show()

# noun = sns.barplot(x=noun['Word'], y=noun['Index'])
# noun.set_xticklabels(noun.get_xticklabels(), rotation=50)
# plt.title('Most Common Nouns')
# plt.show()
#
# verb = sns.barplot(x=verb['Word'], y=verb['Index'])
# verb.set_xticklabels(verb.get_xticklabels(), rotation=50)
# plt.title('Most Common Verbs')
# plt.show()

