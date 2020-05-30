
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from GraphQDMR.CanonicalizerQDMR.CanonicalizationRules import CANONICALIZATION_RULES

class CanonicalizerQDMR:
    LANGUAGE        =   'english'
    
    @staticmethod
    def convert_to_common_case(step_desc):
        return step_desc.lower() 
    
    # Normalization Section
    @staticmethod
    def normalize(step_desc, language = None):
        normalized_step_desc    = CanonicalizerQDMR.convert_to_common_case(step_desc)
        # TODO : REVISE
        # normalized_step_desc    = CanonicalizerQDMR.remove_stop_words(normalized_step_desc)
        normalized_step_desc    = CanonicalizerQDMR.steam(normalized_step_desc)
        return normalized_step_desc 

    @staticmethod
    def remove_stop_words(sentence, language = None):
        language            = language if language else CanonicalizerQDMR.LANGUAGE
        stop_words          = set(stopwords.words('english'))   
        word_tokens         = word_tokenize(sentence)           
        filtered_sentence   = [ w for w in word_tokens if not w in stop_words ]
        return ' '.join(filtered_sentence)
    
    @staticmethod
    def steam(sentence, language = None):
        language            = language if language else CanonicalizerQDMR.LANGUAGE
        stemmer             = SnowballStemmer(language, ignore_stopwords=False)
        sentence            = word_tokenize(sentence)
        steamed_sentence    = [ stemmer.stem(word) for word in sentence ]
        return ' '.join(steamed_sentence)
    
    # Canonicalization Section
    # NOTE! Canonicalization includes Normalization     
    @staticmethod
    def canonicalize(step_desc, language = None):
        canonicalized_step_desc = CanonicalizerQDMR.normalize(step_desc, language)
        for pattern_to_replace, replace_token in CANONICALIZATION_RULES:
            canonicalized_step_desc = re.sub(pattern_to_replace, replace_token, canonicalized_step_desc)
        return canonicalized_step_desc
