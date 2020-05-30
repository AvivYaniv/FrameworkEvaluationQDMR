
import pytest
from GraphQDMR.CanonicalizerQDMR.CanonicalizerQDMR import CanonicalizerQDMR

def test_can():
    str_tups    =   \
    [               \
        ('sabich', 'sabich'), 
    ]
    str_tups = [ (CanonicalizerQDMR.canonicalize(s1), CanonicalizerQDMR.canonicalize(s2)) for s1, s2 in str_tups]
    def compare(s1, s2):
        return s1 == s2
    for (s1, s2) in str_tups:
        assert compare(s1, s2), f'Compare failed on {s1} != {s2}'