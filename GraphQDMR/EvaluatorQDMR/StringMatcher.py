
from alignment.sequence import Sequence
from alignment.vocabulary import Vocabulary
from alignment.sequencealigner import SimpleScoring, GlobalSequenceAligner

def get_string_match_score(string1, string2, letters_sequence = True):

    if letters_sequence:
        seq1 = string1
        seq2 = string2
    else:
        seq1 = string1.split(" ")
        seq2 = string2.split(" ")

    return get_sequences_match_score(seq1, seq2)

def get_sequences_match_score(seq1, seq2):
    a = Sequence(seq1)
    b = Sequence(seq2)

    # Create a vocabulary and encode the sequences.
    v = Vocabulary()
    aEncoded = v.encodeSequence(a)
    bEncoded = v.encodeSequence(b)

    # Create a scoring and align the sequences using global aligner.
    scoring = SimpleScoring(2, -1)
    aligner = GlobalSequenceAligner(scoring, -2)
    score, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)
    alignment = v.decodeSequenceAlignment(encodeds[0])

    return 1 - alignment.percentSimilarity()/100
