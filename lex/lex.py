"""
docs

"""

import pickle
import re
import math
import pkgutil
from pkg_resources import resource_filename
from nltk.corpus import wordnet


__version__ = '0.1'
__author__ = 'ELI Data Mining Group'

FILE_MAP = {
    'NGSL': resource_filename('lextools', 'data/wordlists/ngsl_2k.txt'),
    'PET': resource_filename('lextools', 'data/wordlists/pet_coca_2k.txt'),
    'PELIC': resource_filename('lextools', 'data/wordlists/pelic_l3_2k.txt')
}

# lookup table created from NGSL and spaCy word lists
LOOKUP = pickle.loads(pkgutil.get_data('lextools', 'data/lemmatizer.pkl'))
def lemmatize(tokens):
    """ Lemmatize with lookup table and return list of corresponding lemmas """
    return [LOOKUP.get(x, x) for x in tokens]


def re_tokenize(text):
    """
    Returns a list of tokens from input text
    Lowercase input, removing symbols and digits.
    """
    return re.findall(r"[A-Za-z]+", text.lower())


def adv_guiraud(text, freq_list='NGSL', custom_list=None, spellcheck=True):
    """
    Calculates advanced guiraud: advanced types / sqrt(number of tokens)
    By default, uses NGSL top 2k words as frequency list
    custom_list is a custom list of common types for frequency list
    """


    if custom_list is not None:
        if not isinstance(custom_list, list):
            raise TypeError('Please specify a list of strings for custom_list')
        common_types = set(custom_list)
    else:
        if freq_list not in FILE_MAP:
            raise KeyError \
                    ('Please specify an appropriate frequency list with' \
                    'custom_list or set freq_list to one of NGSL, PET, PELIC.')
        with open(FILE_MAP[freq_list]) as f_in:
            common_types = set([x.strip() for x in f_in.readlines()])


    tokens = re_tokenize(text)

    if len(tokens) == 0:
        return 0

    advanced = set()
    for token in tokens:
        lemma = LOOKUP.get(token, token)
        if lemma not in common_types and (not spellcheck or wordnet.synsets(lemma)):
            advanced.add(lemma)

    return len(advanced)/math.sqrt(len(tokens))