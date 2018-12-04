# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following script takes parsed documents and returns the top 100 verbs, nouns, and adjectives
occurring in each document, including frequency, rate, coca rate, and coca index

Required inputs:
    -Parsed spacy document(s)
"""

import textacy
from textacy.extract import pos_regex_matches
import pandas as pd
import pickle


def top_pos(row, pattern, remove=list()):
    from nltk.corpus import stopwords
    all_stop = set(stopwords.words('english'))
    pos = list(token.lemma_ for token in
               textacy.extract.pos_regex_matches(row, pattern))
    pos = " ".join(word for word in pos if word not in remove and word not in all_stop)
    return pos


def count_pos(series, n):
    from nltk import word_tokenize
    from nltk import FreqDist
    series = series.str.cat(sep=' ')
    words = word_tokenize(series)
    word_dist = FreqDist(words)
    rslt = pd.DataFrame(word_dist.most_common(n),
                        columns=['Word', 'Frequency'])
    return rslt


def coca_rate(df):
    df_sum = sum(df['Frequency'])
    df['Rate'] = df['Frequency'].apply(lambda row: row/df_sum)
    df = df.merge(coca, how='left', left_on='Word', right_on='word')
    df['Index'] = 'placeholder'
    df['Index'] = df['Rate'].apply(lambda row: row/df['rate'])
    df['Index'] = df['Index'].apply(lambda row: row * 100)
    return df


# MAIN #
ROOTDIR = "C:\\Users\\samantha.riley\\PycharmProjects\\Farxiga\\Pickles\\Analysis Pickles\\"

# load coca
with open(ROOTDIR + 'COCA_Rate_No_Stopwords.pickle', 'rb') as handle:
    coca = pickle.load(handle)

# load data
with open(ROOTDIR + 'parsed_all_sents.pickle', 'rb') as handle:
    df = pickle.load(handle)

# make new columns with all pos extractions
df['verbs'] = df['parsed'].apply(lambda row: top_pos(row, r'<VERB>', remove = ['be', 'have', 'take', 'farxiga']))
df['adjs'] = df['parsed'].apply(lambda row: top_pos(row, r'<ADJ>', remove = ['-PRON-', 'mg', 'farxiga', 'janssen']))
df['nouns'] = df['parsed'].apply(lambda row: top_pos(row, r'<NOUN>'))

# count frequency of each pos, calculate rate of incidence
# import coca rate and calculate index for each pos
# returns a dataframe with the top 100 pos by frequency
adj = coca_rate(count_pos(df['adjs'], 100))
verb = coca_rate(count_pos(df['verbs'], 100))
noun = coca_rate(count_pos(df['nouns'], 100))

# concatenate above pos dataframes into a final frame with pos as dimension column
adj['pos'] = 'adj'
verb['pos'] = 'verb'
noun['pos'] = 'noun'
final = pd.concat([adj, verb, noun], ignore_index=True)

with open(r"C:\\Users\\samantha.riley\\PycharmProjects\\Farxiga\\Final Deck\\pos\\pos.pickle", "wb") as handle:
    pickle.dump(final, handle, protocol=pickle.HIGHEST_PROTOCOL)

