# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following is a basic script to make a scattertext word similarity explorer.

Required inputs:
    -Either text or parsed spacy docs in pandas form
    -It will re-parse in order to build the similarity explorer
"""

import spacy
import pickle
import scattertext as st
import pandas as pd

# FILES #
ROOTDIR = "C:\\Users\\samantha.riley\\Alpha Files\\"

Column = "Segment"
Category1 = "De 18 a 24"
Category2 = "Base"
Target = "calidad"

array = [Category1, Category2]

with open(ROOTDIR + 'NYX_dedup.pickle', 'rb') as handle:
    df = pickle.load(handle)

df['Segment'] = pd.np.where(df['Age'] == 'De 18 a 24', 'De 18 a 24', 'Base')

master = df
# master = df.loc[df[Column].isin(array)]

nlp = spacy.load('es_core_news_sm')

corpus = st.CorpusFromPandas(master, category_col=Column,text_col='Post', nlp=nlp).build()

html = st.word_similarity_explorer(corpus,
                                   category=Category1,
                                   category_name=Category1,
                                   not_category_name=Category2,
                                   target_term=Target,
                                   minimum_term_frequency=1,
                                   pmi_threshold_coefficient=4,
                                   width_in_pixels=1000,
                                   nlp=nlp,
                                   alpha=0.01,
                                   max_p_val=0.05,
                                   save_svg_button=True)

file_name = ROOTDIR + Column + '_' + Category1 + '_' + Category2 + '_dup_wordsimilarity.html'
open(file_name, 'wb').write(html.encode('utf-8'))

