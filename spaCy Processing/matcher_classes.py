# -*- coding: utf-8 -*-
"""
@author: samantha.riley

The following classes are custom tagger objects that take a list of
words or phrases and run over a parsed document applying appropriate tags,
both to the tokens themselves, and to the sentences that contain the tokens,
which makes it easy to extract those sentences later.

Each PhraseMatcher pre-processing step is added to the spacy parsing
pipeline; the "out of the box" pipeline includes typical things like
tokenizer, tagger, named entity recognition, etc. You can insert
custom processes into the pipeline before parsing text documents, such
as the below (flagging custom keywords and sentences for later extraction).

Required inputs:
    -List of seed terms to flag tokens and categorize desired sentences

Notes:
    These classes should be imported into whatever script you're writing
    for the initial spacy parse, so you can insert the components into the
    spacy nlp pipeline before running text documents through
"""

from spacy.matcher import PhraseMatcher
from spacy.tokens import Span, Token


class DrugRecognizer(object):
    name = 'drug_tag'

    def __init__(self, nlp, label='PRODUCT'):
        drugs = ['humalog', 'insulin', 'byetta', 'lantus', 'tradjenta', 'metformin', 'victoza', 'jardiance', 'novolog',
                 'farxiga', 'actos', 'invokana', 'levemir', 'januvia', 'trulicity', 'bydureon', 'aspirin',
                 'glimeperide','amaryl', 'glipizide', 'janumet', 'oseni', 'glucotrol', 'glucophage', 'exenatide',
                 'liraglutide','albiglutide', 'tanzeum', 'dulaglutide', 'empagliflozin', 'sulfonylureas', 'dapagliflozin',
                 'repaglinide','prandin', 'gliclazide', 'glyburide', 'canagliflozin', 'sitagliptin', 'meglitinide',
                 'nateglinide','starlix', 'onglyza', 'glumetza', 'fortamet', 'riomet', 'thiazolidinediones ',
                 'glimepiride','rosiglitazone','xigduo', 'glyxambi', 'synjardy', 'linagliptin', 'pioglitazone',
                 'bromocriptine', 'parlodel','actoplus','micronase', 'humalin', 'chlorpropamide', 'diabinese', 'glynase',
                 'acarbose', 'invokamet','saxagliptin','diabeta', 'tolinase', 'tolazamide', 'orinase', 'tolbutamide',
                 'tol-tab', 'glucovance']

        self.label = nlp.vocab.strings[label]
        patterns = [nlp(i.lower()) for i in drugs]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('DRUG_NAMES', None, *patterns)

        Token.set_extension('is_drug', default=False)
        Token.set_extension('is_farxiga', default=False)
        Token.set_extension('is_biguanide', default=False)
        Token.set_extension('is_sglt2', default=False)
        Token.set_extension('is_dpp4', default=False)
        Token.set_extension('is_glp1', default=False)

        Span.set_extension('has_drug', getter=self.has_drug)
        Span.set_extension('has_biguanide', getter=self.has_biguanide)
        Span.set_extension('has_sglt2', getter=self.has_sglt2)
        Span.set_extension('has_glp1', getter=self.has_glp1)
        Span.set_extension('has_dpp4', getter=self.has_dpp4)
        Span.set_extension('has_farxiga', getter=self.has_farxiga)

    def __call__(self, doc):
        BIGUANIDE = ['metformin', 'glipizide', 'janumet', 'glucophage', 'empagliflozin', 'glyburide', 'glumetza', 'fortamet', 'riomet', 'rosiglitazone', 'xigduo', 'synjardy', 'pioglitazone', 'actoplus', 'invokamet', 'glucovance']
        SGLT2 = ['jardiance', 'farxiga', 'invokana', 'dapagliflozin', 'canagliflozin']
        GLP1 = ['byetta', 'victoza', 'trulicity', 'bydureon', 'exenatide', 'liraglutide', 'albiglutide', 'tanzeum', 'dulaglutide']
        DPP4 = ['tradjenta', 'januvia', 'oseni', 'sitagliptin', 'onglyza', 'glyxambi', 'linagliptin', 'saxagliptin']
        matches = self.matcher(doc)
        entities = []
        for id, start, end in matches:
            entity = Span(doc, start, end, label=self.label)
            entities.append(entity)
            for token in entity:
                token._.set('is_drug', True)
                if token.text in BIGUANIDE:
                    token._.set('is_biguanide', True)
                if token.text in SGLT2:
                    token._.set('is_sglt2', True)
                if token.text in DPP4:
                    token._.set('is_dpp4', True)
                if token.text in GLP1:
                    token._.set('is_glp1', True)
                if token.text == 'farxiga':
                    token._.set('is_farxiga', True)
            doc.ents = list(doc.ents) + [entity]
        for entity in entities:
            entity.merge()
        return doc

    def has_drug(self, tokens):
        return any([t._.get('is_drug') for t in tokens])

    def has_biguanide(self, tokens):
        return any([t._.get('is_biguanide') for t in tokens])

    def has_sglt2(self, tokens):
        return any([t._.get('is_sglt2') for t in tokens])

    def has_glp1(self, tokens):
        return any([t._.get('is_glp1') for t in tokens])

    def has_dpp4(self, tokens):
        return any([t._.get('is_dpp4') for t in tokens])

    def has_farxiga(self, tokens):
        return any([t._.get('is_farxiga') for t in tokens])


class DoctorRecognizer(object):
    name = 'hcp_tag'

    def __init__(self, nlp, label='EVENT'):
        hcp = ['doctor', 'checkup', 'check up', 'appointment', 'physician', 'dietitian', 'nutritionist',
               'dietetic', 'primary care provider', 'primary care', 'specialist', 'endo', 'endocrinologist',
               'podiatrist', 'nephrologist', 'hospital', 'eye doctor', 'optician', 'doctors', 'ER', 'emergency room',
               'nurse', 'pharmacist', 'endocrinology', 'podiatry', 'nephrology']

        self.label = nlp.vocab.strings[label]
        patterns = [nlp(i.lower()) for i in hcp]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('HCP_NAMES', None, *patterns)

        Token.set_extension('is_hcp', default=False)
        Span.set_extension('has_hcp', getter=self.has_hcp)

    def __call__(self, doc):
        matches = self.matcher(doc)
        entities = []
        for id, start, end in matches:
            entity = Span(doc, start, end, label=self.label)
            entities.append(entity)
            for token in entity:
                token._.set('is_hcp', True)
            doc.ents = list(doc.ents) + [entity]
        for entity in entities:
            entity.merge()
        return doc

    def has_hcp(self, tokens):
        return any([t._.get('is_hcp') for t in tokens])


class SideEffectsRecognizer(object):
    name = 'side_effects_tag'

    def __init__(self, nlp):
        side_effects = ['agree with my stomach', 'stomach ache', 'stomach hurts', 'stomach hurting', 'stomach upset',
                        'dizziness', 'dizzy', 'shivering', 'cold sweats', 'stomach cramps', 'stomach cramping',
                        'cramping','nauseous', 'nausea', ' gas', 'gassy', 'bloat', 'bloating', 'weight gain', 'cramps',
                        'side effect','side effects', 'indigestion', 'constipation', 'constipated', 'upset stomach',
                        'skin rash','rash','itching', 'itchy', 'itch', 'metal taste', 'taste metal', 'diarrhea ',
                        'anemia', 'anemic']

        patterns = [nlp(i.lower()) for i in side_effects]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('SIDE_EFFECTS', None, *patterns)

        Token.set_extension('is_se', default=False)
        Span.set_extension('has_se', getter=self.has_se)

    def __call__(self, doc):
        matches = self.matcher(doc)
        side_effects = []
        for id, start, end in matches:
            effect = Span(doc, start, end)
            side_effects.append(effect)
            for token in effect:
                token._.set('is_se', True)
        for effect in side_effects:
            effect.merge()
        return doc

    def has_se(self, tokens):
        return any([t._.get('is_se') for t in tokens])


class DiabetesRecognizer(object):
    name = 'diabetes_tag'

    def __init__(self, nlp):
        diabetes = ['diabetes', 'my diabetes', 'diabetic experience', 'diabetic story', 'diabetes story',
                    'diabetes experience', 'experience with diabetes', 'experience of diabetes',
                    'feelings about diabetes', 'being diabetic','having diabetes']

        patterns = [nlp(i.lower()) for i in diabetes]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('DIABETES', None, *patterns)

        Token.set_extension('is_diabetes', default=False)
        Span.set_extension('has_diabetes', getter=self.has_diabetes)

    def __call__(self, doc):
        matches = self.matcher(doc)
        diabetes = []
        for id, start, end in matches:
            dia = Span(doc, start, end)
            diabetes.append(dia)
            for token in dia:
                token._.set('is_diabetes', True)
        for dia in diabetes:
            dia.merge()
        return doc

    def has_diabetes(self, tokens):
        return any([t._.get('is_diabetes') for t in tokens])

class EmotionRecognizer(object):
    name = 'emotion_tag'

    def __init__(self, nlp):
        emotions = ['abominable', 'admiration', 'affectionate', 'afraid', 'aggressive', 'agonize', 'alarm', 'alienate',
                    'alone', 'amaze', 'angry', 'anguish', 'animate', 'annoy', 'anxious', 'appall', 'ashamed', 'admire',
                    'attract', 'bitter', 'bless', 'boil', 'bore', 'brave', 'calm', 'cheerful', 'clever', 'comfortable',
                    'confident', 'confuse', 'content', 'cowardly', 'crush', 'curious', 'dare', 'deject', 'delight',
                    'depress', 'deprive', 'desolate', 'despair', 'desperate', 'despicable', 'detestable', 'devastate',
                    'diminish', 'disappoint', 'discourage', 'disgust', 'disillusion', 'disinterested', 'dismay',
                    'dissatisfy', 'distress', 'distrustful', 'doubtful', 'dull', 'dynamic', 'eager', 'earnest',
                    'ecstatic', 'elate', 'embarrass', 'empty', 'encourage', 'engross', 'enrage', 'enthusiastic',
                    'excite', 'fascinate', 'fatigue', 'fearful', 'festive', 'force', 'fortunate', 'frighten', 'fear',
                    'frustrate', 'fume', 'glad', 'gleeful', 'grateful', 'grief', 'grieve', 'guilty', 'happy',
                    'hardy', 'hateful', 'heartbroken', 'helpless', 'hesitant', 'hopeful', 'hostile', 'humiliate',
                    'impulsive', 'incapable', 'incense', 'indecisive', 'indifferent', 'indignant', 'inferior',
                    'inflame', 'infuriate', 'injure', 'inquisitive', 'insensitive', 'inspire', 'insult', 'intrigue',
                    'irritate', 'joyous', 'jubilant', 'keen', 'liberate', 'lifeless', 'lonely', 'glee',
                    'lousy', 'love', 'lucky', 'mad', 'menace', 'merry', 'miserable', 'misgiving', 'humiliating',
                    'mournful', 'nervous', 'neutral', 'nonchalant', 'nosy', 'offend', 'offensive', 'optimistic',
                    'overjoyed', 'panic', 'paralyze', 'passionate', 'pathetic', 'peaceful', 'perplex', 'pessimistic',
                    'playful', 'powerless', 'preoccupy', 'provoke', 'quake', 'reassure', 'rebellious',
                    'reject', 'relax', 'repugnant', 'resentful', 'restless', 'sad', 'satisfy', 'scare',
                    'insecure', 'serene', 'shaky', 'shy', 'skeptical', 'snoopy', 'sorrowful', 'spirit', 'stigmatize',
                    'stigma', 'strong', 'stupefy', 'sulky', 'suspicious', 'sympathetic', 'sympathy', 'tearful',
                    'tenacious', 'tender', 'tense', 'terrible', 'terrify', 'thankful', 'threaten', 'thrill', 'timid',
                    'torment', 'torture', 'tragic', 'unbelieving', 'uncertain', 'understand', 'uneasy',
                    'unhappy', 'unique', 'unpleasant', 'unsure', 'upset', 'useless', 'victimize', 'vulnerable',
                    'wary', 'weary', 'woeful', 'wonderful', 'worry', 'agonized', 'alarmed', 'alienated', 'amazed',
                    'animated', 'annoyed', 'appalled', 'attracted', 'blessed', 'boiling', 'bored', 'confused',
                    'crushed', 'daring', 'dejected', 'delighted', 'depressed', 'deprived', 'devastated', 'diminished',
                    'disappointed', 'discouraged', 'disgusting', 'disillusioned', 'dismayed', 'dissatisfied',
                    'distressed', 'elated', 'embarrassed', 'encouraged', 'engrossed', 'enraged', 'excited',
                    'fascinated', 'fatigued', 'forced', 'frightened', 'frustrated', 'fuming', 'grieved',
                    'humiliated', 'incensed', 'inflamed', 'infuriated', 'injured', 'inspired', 'insulting',
                    'intrigued', 'irritated', 'liberated', 'glee ', 'menaced', 'offended', 'paralyzed',
                    'perplexed', 'preoccupied', 'provoked', 'quaking', 'reassured', 'rejected', 'relaxed',
                    'satisfied', 'scared', 'spirited', 'stigmatized', 'stupefied', 'terrified', 'threatened',
                    'thrilled', 'tormented', 'tortured', 'understanding', 'victimized', 'worried']

        patterns = [nlp(i) for i in emotions]
        self.matcher = PhraseMatcher(nlp.vocab)
        self.matcher.add('EMOTIONS', None, *patterns)

        Token.set_extension('is_emotion', default=False)
        Span.set_extension('has_emotion', getter=self.has_emotion)

    def __call__(self, doc):
        matches = self.matcher(doc)
        emotions = []
        for id, start, end in matches:
            em = Span(doc, start, end)
            emotions.append(em)
            for token in em:
                token._.set('is_emotion', True)
        for em in emotions:
            em.merge()
        return doc

    def has_emotion(self, tokens):
        return any([t._.get('is_emotion') for t in tokens])
