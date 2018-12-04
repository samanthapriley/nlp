# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following is one of two ways to extract patterns from parsed spacy docs.
This way uses the spacy matcher object to specify patterns of tokens to
extract from the doc.

Required inputs:
    -Parsed spacy document(s)
    -Desired pattern for extraction

Notes:
    "*" is spacy notation for "optional." There are many
    token attributes you can match for, including the lemma form of the token,
    the lowercase form of the token, the part of speech, and the entity type.
"""

import spacy
from spacy.matcher import Matcher
import pickle
import pandas as pd

# ### Matching Sents ###
nlp = spacy.load('en_core_web_sm')


def diabetes_is(doc):
    matched_sents = []
    matcher = Matcher(nlp.vocab)
    pattern = [{'LOWER': 'diabetes'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
               {'POS': 'ADJ'}, {'OP': '*'}]
    matcher.add('DiabetesIs', None, pattern)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]  # the matched span
        matched_sents.append(span.text)
    sents = ",".join(item for item in matched_sents)
    return sents


def verb_doc(doc):
    matched_sents = []
    matcher = Matcher(nlp.vocab)
    pattern = [{'LEMMA': 'ASK'}, {'POS': 'ADJ', 'OP': '*'}, {'POS': 'PRON', 'OP': '*'}, {'LOWER': 'doctor'}]
    matcher.add('Diabetes', None, pattern)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]  # the matched span
        matched_sents.append(span.sent)
    sents = ",".join(sent.text for sent in matched_sents)
    return sents


def verb_diabetes(doc):
    matched_sents = []
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'VERB'},{'POS': 'ADJ', 'OP': '*'}, {'POS': 'DET', 'OP': '*'}, {'POS': 'PRON', 'OP': '*'},
               {'LOWER': 'diabetes'}]
    matcher.add('Diabetes', None, pattern)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]  # the matched span
        matched_sents.append(" ".join(word.lemma_ for word in span))
    sents = ",".join(item for item in matched_sents)
    return sents


# MAIN #
with open(r'C:\Users\samantha.riley\PycharmProjects\Farxiga\Pickles\Analysis Pickles\
edited_target1_parsed_less_stacked_df.pickle', 'rb') as handle:
    t = pickle.load(handle)

with open(r'C:\Users\samantha.riley\PycharmProjects\Farxiga\Pickles\Analysis Pickles\
edited_base3_parsed_less_stacked_df.pickle', 'rb') as handle:
    b = pickle.load(handle)
with open(r'C:\Users\samantha.riley\PycharmProjects\Farxiga\Pickles\Analysis Pickles\
edited_base4_parsed_less_stacked_df.pickle', 'rb') as handle:
    b2 = pickle.load(handle)

data = pd.concat([t, b, b2], ignore_index=True)
data['verb_doc'] = data['parsed'].apply(verb_doc)
data.to_csv('data.csv')

