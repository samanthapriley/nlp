# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following is a basic script to make a scattertext from text (string) documents.

Required inputs:
    -Text in pandas dataframe
"""


import scattertext as st
import pandas as pd


# FILES #
array = ['Biotherm', 'Biotherm Homme']
df = pd.DataFrame(pd.read_excel(r'C:\Users\samantha.riley\Alpha Files\el_corte_ingles.xlsx'))

master = df.loc[df['Brand'].isin(array)]


# # SCATTERTEXT EXPLORER #
import spacy
nlp = spacy.load('es_core_news_sm')
corpus = st.CorpusFromPandas(master, category_col='Brand', text_col='Post', nlp=nlp).build()
html = st.produce_scattertext_explorer(corpus,
                                       category='Biotherm Homme',
                                       category_name='Biotherm Homme',
                                       not_category_name='Biotherm',
                                       width_in_pixels=1000, metadata=None, show_top_terms = True)

file_name = r'C:\Users\samantha.riley\Alpha Files\biotherm_scattertext.html'
open(file_name, 'wb').write(html.encode('utf-8'))

term_freq_df = corpus.get_term_freq_df()

term_freq_df['Biotherm Homme Score'] = \
corpus.get_scaled_f_scores('Biotherm Homme')

term_freq_df['Biotherm'] = \
corpus.get_scaled_f_scores('Biotherm')

term_freq_df.to_excel(r"C:\Users\samantha.riley\Alpha Files\biotherm_termfreq.xlsx")

