# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following is a basic script to make a scattertext from already parsed documents.

Required inputs:
    -parsed spacy docs in pandas form
"""


import scattertext as st
from scattertext import FeatsFromSpacyDoc
import pickle

# FILES #

with open(r'C:\Users\samantha.riley\Alpha Files\elcorte.pickle', 'rb') as handle:
    df = pickle.load(handle)

Column = "Brand"
Category1 = "Yves Saint Laurent"
Category2 = "Lancôme"

array = [Category1, Category2]

master = df.loc[df[Column].isin(array)]

# # SCATTERTEXT EXPLORER #
import spacy
nlp = spacy.load('es_core_news_sm')
corpus = st.CorpusFromParsedDocuments(master, category_col=Column, parsed_col='Parsed', feats_from_spacy_doc=FeatsFromSpacyDoc()).build()
html = st.produce_scattertext_explorer(corpus,
                                       category=Category1,
                                       category_name=Category1,
                                       not_category_name=Category2,
                                       width_in_pixels=1000, metadata=None, show_top_terms = True)

file_name = 'C:\\Users\\samantha.riley\\Alpha Files\\' + Column + '_' + Category1 + '_' + Category2 + '_scattertext.html'
open(file_name, 'wb').write(html.encode('utf-8'))

term_freq_df = corpus.get_term_freq_df()

term_freq_df[Category1 + ' Score'] = \
corpus.get_scaled_f_scores(Category1)

term_freq_df[Category2 + ' Score'] = \
corpus.get_scaled_f_scores(Category2)

term_freq_df.to_excel('C:\\Users\\samantha.riley\\Alpha Files\\' + Column + '_' + Category1 + '_' + Category2 + "_termfreq.xlsx")
