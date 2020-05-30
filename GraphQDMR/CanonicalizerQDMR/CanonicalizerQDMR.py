
import re

import nltk

## NOTE! NOTE! NOTE! NOTE! NOTE! < RUN OF FIRST EXECUTION > NOTE! NOTE! NOTE! NOTE! NOTE! 
# nltk.download()

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
    def normalize(step_desc, language = None):
        normalized_step_desc    = CanonicalizerQDMR.convert_to_common_case(step_desc)
        # TODO : REVISE
        # normalized_step_desc    = CanonicalizerQDMR.remove_stop_words(normalized_step_desc)
        normalized_step_desc    = CanonicalizerQDMR.steam(normalized_step_desc)
        normalized_step_desc    = CanonicalizerQDMR.normalize_whitespaces(normalized_step_desc)
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
    def canonicalize(step_desc, language = None):
        print(f'TODO DEBUG REMOVE : Original [{step_desc}]')
        canonicalized_step_desc = CanonicalizerQDMR.normalize(step_desc, language)
        print(f'TODO DEBUG REMOVE : Normalized [{step_desc}]')
        for pattern_to_replace, replace_token in CANONICALIZATION_RULES.items():
            canonicalized_step_desc = re.sub(pattern_to_replace, replace_token, canonicalized_step_desc)
        print(f'TODO DEBUG REMOVE : Canonicalized [{step_desc}]')
        canonicalized_step_desc = CanonicalizerQDMR.normalize_whitespaces(canonicalized_step_desc)
        print(f'TODO DEBUG REMOVE : Final [{step_desc}]') 
        return canonicalized_step_desc