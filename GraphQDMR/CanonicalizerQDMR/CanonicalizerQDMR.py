
import re

import nltk

## NOTE! NOTE! NOTE! NOTE! NOTE! < RUN OF FIRST EXECUTION > NOTE! NOTE! NOTE! NOTE! NOTE! 
# nltk.download()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from GraphQDMR.CanonicalizerQDMR.CanonicalizationRules import CANONICALIZATION_RULES

import logging, sys
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='%(levelname)s - %(message)s @ %(filename)s')

class CanonicalizerQDMR:
    LANGUAGE        =   'english'
    
    @staticmethod
    def convert_to_common_case(step_desc):
        return step_desc.lower() 
    
    @staticmethod
    def resolve_language(language = None):
        return language if language else CanonicalizerQDMR.LANGUAGE

    @staticmethod
    def normalize_whitespaces(sentence):
        sentence = sentence.replace('{ }', '{}')
        sentence = sentence.strip()
        return re.sub(' +', ' ', sentence)
    
    # Normalization Section
    @staticmethod
    def normalize(step_desc, remove_references = True, remove_stopwords = True, language = None):
        normalized_step_desc        = CanonicalizerQDMR.convert_to_common_case(step_desc)
        if remove_references:
            normalized_step_desc    = normalized_step_desc.replace('{}', '')
        if remove_stopwords:
            normalized_step_desc    = CanonicalizerQDMR.remove_stop_words(normalized_step_desc)
        normalized_step_desc        = CanonicalizerQDMR.steam(normalized_step_desc)
        normalized_step_desc        = CanonicalizerQDMR.normalize_whitespaces(normalized_step_desc)
        return normalized_step_desc 

    @staticmethod
    def remove_stop_words(sentence, language = None):
        language            = CanonicalizerQDMR.resolve_language(language)
        stop_words          = set(stopwords.words('english'))   
        word_tokens         = word_tokenize(sentence)           
        filtered_sentence   = [ w for w in word_tokens if not w in stop_words ]
        return ' '.join(filtered_sentence)
    
    @staticmethod
    def steam(sentence, language = None):
        language            = CanonicalizerQDMR.resolve_language(language)
        stemmer             = SnowballStemmer(language, ignore_stopwords=False)
        sentence            = word_tokenize(sentence)
        steamed_sentence    = [ stemmer.stem(word) for word in sentence ]
        return ' '.join(steamed_sentence)
    
    # Canonicalization Section
    # NOTE! Canonicalization includes Normalization     
    @staticmethod
    def canonicalize(step_desc, remove_references = True, remove_stopwords = True, language = None):
        logging.debug(f'Original [{step_desc}]') 
        canonicalized_step_desc = CanonicalizerQDMR.normalize(step_desc, remove_references, remove_stopwords, language)
        logging.debug(f'Normalized [{step_desc}]')
        for pattern_to_replace, replace_token in CANONICALIZATION_RULES.items():
            canonicalized_step_desc = re.sub(pattern_to_replace, replace_token, canonicalized_step_desc)
        logging.debug(f'Canonicalized [{step_desc}]')
        canonicalized_step_desc = CanonicalizerQDMR.normalize_whitespaces(canonicalized_step_desc)
        logging.debug(f'Final [{step_desc}]') 
        return canonicalized_step_desc
