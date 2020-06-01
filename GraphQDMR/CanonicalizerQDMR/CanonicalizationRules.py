
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
{   
    # Keyword EXIST_ANY Section
    r'if exist'      : KeywordQDMR.EXIST_ANY.get_id(),
    r'if any'        : KeywordQDMR.EXIST_ANY.get_id(),
    r'if any exist'  : KeywordQDMR.EXIST_ANY.get_id(),
    r'if there is'   : KeywordQDMR.EXIST_ANY.get_id(),
    r'if there are'  : KeywordQDMR.EXIST_ANY.get_id(),
    r'is there any'  : KeywordQDMR.EXIST_ANY.get_id(),
    
    # Keyword TO Section
    r'\bto\b'        : KeywordQDMR.TO.get_id(),
    
    # Keyword FROM Section
    r'\bfrom\b'      : KeywordQDMR.FROM.get_id(),    
}   
