__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Sep 27, 2013"

import sys
from collections import defaultdict
import math
from count_freqs import Hmm

def problem4():
    '''problem 4 main code'''
    try:
        input = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    # create hmm
    counter = Hmm(3)
    counter.read_counts(input)
    #counter.emission_counts[('mind','O')]  #6
    emission_param('Carnival','I-MISC', counter)

    # Then print counts for all ngrams
    n = 1
    for ngram in counter.ngram_counts[n-1]:
        ngramstr = " ".join(ngram)
        print "%i %i-GRAM %s\n" %(counter.ngram_counts[n-1][ngram], n, ngramstr)
        print counter.ngram_counts[n-1][ngram], n, ngramstr

def emission_param(x,y,hmm_obj):
    '''computes the ratio emission count to unigram count'''
    # y is tag (ie IORG) while x is word
    print x, y
    print hmm_obj.emission_counts[(x,y)]
    print hmm_obj.ngram_counts[0][x]
    print hmm_obj.ngram_counts[0][y]

if __name__ == "__main__":
    problem4()