
import re

import nltk

## NOTE! NOTE! NOTE! NOTE! NOTE! < RUN OF FIRST EXECUTION > NOTE! NOTE! NOTE! NOTE! NOTE! 
# nltk.download()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

from GraphQDMR.CanonicalizerQDMR.CanonicalizationRules import CANONICALIZATION_KEEPER_RULES
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
    def normalize(step_desc, remove_references = None, remove_stopwords = None, language = None):
        normalized_step_desc        = CanonicalizerQDMR.convert_to_common_case(step_desc)
        if (remove_references if remove_references else True):
            normalized_step_desc    = normalized_step_desc.replace('{}', '')
        normalized_step_desc        = CanonicalizerQDMR.steam(normalized_step_desc)
        if (remove_stopwords if remove_stopwords else True):
            normalized_step_desc    = CanonicalizerQDMR.remove_stop_words(normalized_step_desc)
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
    def canonicalize(step_desc, remove_references = None, remove_stopwords = None, language = None):
        canonicalized_step_desc = step_desc
        logging.debug(f'Original [{canonicalized_step_desc}]')
        # First, replace stop-words combinations, that match to known keywords (i.e. 'if there any' is of keyword ANY_EXIST, under operation BOOLEAN)
        # thus keywords serve as a canonicalized form to compare meaningful relations (that are more specific than OPERATION)
        for pattern_to_replace, replace_token in CANONICALIZATION_KEEPER_RULES.items():
            canonicalized_step_desc = re.sub(pattern_to_replace, replace_token, canonicalized_step_desc)
            logging.debug(f'Keyworded [{canonicalized_step_desc}]')
        # Normalize, possibly removing references and stop-words, accordign to flag  
        canonicalized_step_desc = CanonicalizerQDMR.normalize(canonicalized_step_desc, remove_references, remove_stopwords, language)
        logging.debug(f'Normalized [{canonicalized_step_desc}]')
        # Convert to  Canonicalized form, by changing patterns (most important to clean special stop-words when remove_stopwords is false) 
        for pattern_to_replace, replace_token in CANONICALIZATION_RULES.items():
            canonicalized_step_desc = re.sub(pattern_to_replace, replace_token, canonicalized_step_desc)
        logging.debug(f'Canonicalized [{canonicalized_step_desc}]')
        # Removing duplicated white-spaces
        canonicalized_step_desc = CanonicalizerQDMR.normalize_whitespaces(canonicalized_step_desc)
        logging.debug(f'Final [{canonicalized_step_desc}]') 
        return canonicalized_step_desc
