
import pytest

from GraphQDMR.CanonicalizerQDMR.CanonicalizerQDMR import CanonicalizerQDMR

def test_canonicalizer():
    str_tups    =   \
    [   
        # TODO
        # ('cost of {}', 'the cost of {}'), 
        # ('{} that is cheapest', 'cheapest of {}'),
        
        ( '{} from st . paul',              '{} from st. paul'              ),
        ( 'cost of {}',                     'the cost of {}'                ),
        ( '{} that are round trip',         '{} that is round trip'         ),
        ( 'what is {}',                     '{}'                            ),
        ( '{} leaving in the after noon',   '{} leaving after noon'         ),
        ( '{} in the early after noon',     '{} early after noon'           ),
        ( '{} that are after noon',         '{} after noon'                 ),
        ( 'the Redskins',                   'redskins'                      ),        
    ]   
    str_tups = [ (CanonicalizerQDMR.canonicalize(s1), CanonicalizerQDMR.canonicalize(s2)) for s1, s2 in str_tups]
    for (s1, s2) in str_tups:
        assert s1 == s2