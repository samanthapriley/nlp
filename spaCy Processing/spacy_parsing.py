# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following is a script that takes text documents stored in a pandas
dataframe and runs them through a custom edited spacy nlp pipeline
that tags tokens/spans according to custom set extensions.

Required inputs:
    -Pandas dataframe of text documents to parse

Notes:
    The parse function below parses the doc twice- the first time to tag tokens/spans
    as remove/keep, the second to truly parse the doc after those tokens are removed or kept.
    In the future I think it makes sense to use NLTK to do string-level pre-processing, and
    then the resulting text documents are put through spacy only a single time; I just wanted
    to figure out how to do it entirely in spacy.

    "._." is spacy notation for an extension on a spacy object. the "_." offset
    denotes that the tag is applied as an extension on the object and does not
    affect the actual underlying text.
"""

import spacy
import pickle
from flag_tokens import Remove, Reserve
from matcher_classes import DrugRecognizer, DoctorRecognizer, SideEffectsRecognizer, DiabetesRecognizer

# create a list of inputs for the removal/preservation classes
remove = ['Originally posted by']
reserve = ['A1C']

# load the spacy model
nlp = spacy.load('en_core_web_sm')

# add custom pipline elements
nlp.add_pipe(Remove(nlp, remove), first=True)
nlp.add_pipe(Reserve(nlp, reserve), after='flag')
nlp.add_pipe(DiabetesRecognizer(nlp), after='reserve')
nlp.add_pipe(DoctorRecognizer(nlp), after='diabetes_tag')
nlp.add_pipe(SideEffectsRecognizer(nlp), after='hcp_tag')
nlp.add_pipe(DrugRecognizer(nlp), last=True)


# parse the text documents, initially disabling topic tags in the pipeline to save time
# parsed doc is reverted back to list of tokens according to rules
# cleaned list of tokens is re-parsed (see note above about combining NLTK/spacy functionality
# in the future for time-savings
def parse(doc):
    doc = nlp(doc, disable=['diabetes_tag', 'hcp_tag', 'drug_tag', 'side_effects_tag','tagger', 'parser', 'ner'])
    tokens = [token.text for token in doc if token.is_alpha or token._.is_reserved and not token.is_punct and not
    token._.is_removal]
    doc = nlp(' '.join(tokens), disable=['remove', 'reserve'])
    return doc

## MAIN ##

# subset the entire text file by target/base and create a new dataframe column with parsed spacy docs

ROOTDIR = "C:\\Users\\samantha.riley\\PycharmProjects\\Farxiga\\Pickles\\Analysis Pickles\\"

with open(ROOTDIR + 'less_stacked_df.pickle', 'rb') as handle:
    df = pickle.load(handle)

df = df.loc[df['category'] == 'base']
df['parsed'] = df['text'].apply(parse)


with open(ROOTDIR + 'base_parsed_less_stacked_df.pickle', 'wb') as handle:
    pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
