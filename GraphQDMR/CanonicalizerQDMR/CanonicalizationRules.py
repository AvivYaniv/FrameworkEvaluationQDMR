
from GraphQDMR.CanonicalizerQDMR.KeywordQDMR import KeywordQDMR

# Dictionary of <RegExp pattern to be replaced> : <Str to replace with>
# ASSUMPTION: All lower-case
# NOTE: All occurrences will be replaced
CANONICALIZATION_RULES =        \
{                               \
    # Redundant Words Section
    r'^the'         : '',
    
    # REVISE SECTION
    r'\. '          : ' ',
    r'\.'           : '',
    
    r'^what is '    : '',
    
    r'in the'       : '',
    
    r'the '         : '',
    
    r'that is '     : '',
    r'that are '    : '',
    r'that '        : '',
    
    r'of '          : '',
    
    # Operations Canonicalization Section
    # BOOLEAN Operation Canonicalization Section
}


CANONICALIZATION_KEEPER_RULES = \
{                               \
    'if there is'   : KeywordQDMR.EXIST_ANY.name,
    'is there any'  : KeywordQDMR.EXIST_ANY.name,
}

