
import pytest

from GraphQDMR.CanonicalizerQDMR.CanonicalizerQDMR import CanonicalizerQDMR

def compare_canonicalized_tup_list(str_tups, remove_references = None, remove_stopwords = None, language = None):
    str_tups = \
        [                                                                                              
            (                                                                                          
                CanonicalizerQDMR.canonicalize(s1, remove_references, remove_stopwords, language),     
                CanonicalizerQDMR.canonicalize(s2, remove_references, remove_stopwords, language)                                                     
            )                                                                                          
            for s1, s2 in str_tups
        ]                                                                                              
    for (s1, s2) in str_tups:
        assert s1 == s2

def test_canonicalizer():
    str_tups    = \
    [   
        ( '{} from st . paul',              '{} from st. paul'              ),
        ( 'cost of {}',                     'the cost of {}'                ),
        ( '{} that are round trip',         '{} that is round trip'         ),
        ( 'what is {}',                     '{}'                            ),
        ( '{} leaving in the after noon',   '{} leaving after noon'         ),
        ( '{} in the early after noon',     '{} early after noon'           ),
        ( '{} that are after noon',         '{} after noon'                 ),
        ( 'the Redskins',                   'redskins'                      ),        
    ]   
    compare_canonicalized_tup_list(str_tups)
    
def test_canonicalizer_reference_removal():
    str_tups    = \
    [   
        ( 'cost of {}',                     'the cost of {}'                ), 
        ( '{} that is cheapest',            'cheapest of {}'                ),        
    ]   
    compare_canonicalized_tup_list(str_tups, remove_references = True)
    
def test_canonicalizer_stopwords():
    str_tups    = \
    [   
        ( 'is what {}',                     '{}'                            ),        
    ]   
    compare_canonicalized_tup_list(str_tups, remove_stopwords = True)
    