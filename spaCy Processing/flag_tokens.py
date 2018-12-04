# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following two classes are custom tagger objects that take a list of
words or phrases to either keep or remove and run over a parsed document
applying appropriate tags.

spacy differs from nltk in that you can't easily add/delete tokens after
parsing, because the tokens are no longer strings, they're spacy objects.
It's possible to do it but much easier to do token-level manipulation
as a part of the transformation into a spacy document.

Each PhraseMatcher pre-processing step is added to the spacy parsing
pipeline; the "out of the box" pipeline includes typical things like
tokenizer, tagger, named entity recognition, etc. You can insert
custom processes into the pipeline before parsing text documents, such
as the below (flagging words and phrases for removal or preservation).

Required inputs:
    -Knowledge of nuisance words and phrases you want to remove from the data,
    organized in list form
    -Knowledge of words and phrases you know will be removed during other steps
    in the pipeline (e.g. stopwords and punct marks) that you want to flag to
    keep, organized in list form

Notes:
    These classes should be imported into whatever script you're writing
    for the initial spacy parse, so you can insert the components into the
    spacy nlp pipeline before running text documents through
"""

from spacy.matcher import PhraseMatcher
from spacy.tokens import Span, Token

# takes a list of words and/or phrases to flag for removal
# PhraseMatcher combs a parsed document, merges any multi-token removal
# phrases into one token, and tags all tokens for eventual removal


class Remove(object):
    name = 'remove'

    def __init__(self, nlp, remove=tuple()):
        remove = [nlp(i.lower()) for i in remove]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('REMOVE_WORDS', None, *remove)

        Token.set_extension('is_removal', default=False)

    def __call__(self, doc):
        matches = self.matcher(doc)
        removals = []
        for id, start, end in matches:
            removal = Span(doc, start, end)
            removals.append(removal)
            for token in removal:
                token._.set('is_removal', True)
        for removal in removals:
            removal.merge()
        return doc


# takes a list of words and/or phrases to flag for preservation
# PhraseMatcher combs a parsed document, merges any multi-token preservation
# phrases into one token, and tags all tokens that would otherwise be removed by logic
# i.e. stopwords you want to keep, punctuation marks you want to keep, etc.


class Reserve(object):
    name = 'reserve'

    def __init__(self, nlp, reserve=tuple()):
        reserve = [nlp(i.lower()) for i in reserve]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('RESERVE_WORDS', None, *reserve)

        Token.set_extension('is_reserved', default=False)

    def __call__(self, doc):
        matches = self.matcher(doc)
        reserved = []
        for id, start, end in matches:
            reserve = Span(doc, start, end)
            reserved.append(reserve)
            for token in reserve:
                token._.set('is_reserved', True)
        for reserve in reserved:
            reserve.merge()
        return doc




