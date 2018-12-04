# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following takes parsed and custom tagged spacy docs and extracts sentences that were flagged as
containing certain keywords (e.g. sentences about hcps, sentences about drugs, etc).

Required inputs:
    -Parsed and custom tagged spacy docs
"""

import pandas as pd
import pickle


def create_corpora(docs):
    dfs = []
    for doc in docs:
        hcp = " ".join(sent.text for sent in doc.sents if sent._.has_hcp)
        diabetes = " ".join(sent.text for sent in doc.sents if sent._.has_diabetes)
        side_effects = " ".join(sent.text for sent in doc.sents if sent._.has_se)
        farxiga = " ".join(sent.text for sent in doc.sents if sent._.has_farxiga)
        biguanide = " ".join(sent.text for sent in doc.sents if sent._.has_biguanide)
        sglt2 = " ".join(sent.text for sent in doc.sents if sent._.has_sglt2)
        dpp4 = " ".join(sent.text for sent in doc.sents if sent._.has_dpp4)
        glp1 = " ".join(sent.text for sent in doc.sents if sent._.has_glp1)
        dic = {'hcp': hcp, 'diabetes': diabetes, 'side_effects': side_effects, 'farxiga': farxiga,
               'biguanide': biguanide, 'sglt2': sglt2, 'dpp4': dpp4, 'glp1': glp1}
        dfs.append(pd.DataFrame.from_dict(dic, orient='index')
                   .reset_index().rename(columns={'index': 'category', 0: 'text'}))
    df = pd.concat(dfs, ignore_index=True)
    return df

# MAIN #
ROOTDIR = "C:\\Users\\samantha.riley\\Documents\\Farxiga Data\\"

with open(ROOTDIR + 'target_parsed_less_stacked_df.pickle', 'rb') as handle:
    df = pickle.load(handle)

docs = df.parsed.tolist()
df = create_corpora(docs)

with open(ROOTDIR + 'target_sents.pickle', 'wb') as handle:
    pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)


