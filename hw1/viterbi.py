__author__="Emily Schultz <ess2183@columbia.edu>"
__date__ ="$Sep 27, 2013"

import sys
from collections import defaultdict
import math
from count_freqs import Hmm

"""
Implement the Viterbi algorithm to compute
argmax (y1...yn) p(x1...xn, y1...yn)
Your tagger should have the same basic functionality as the baseline tagger.
Instead of emission probabilities the third column should contain the log-probability
of the tagged sequence up to this word.
"""

if __name__ == "__main__":

    if len(sys.argv) != 3: # Expect exactly two arguments: the counts file and dev file
        usage()
        sys.exit(2)

    try:
        counts_file = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    counter = Hmm(3)
    # Read counts
    counter.read_counts(counts_file)

    counter.viterbi_read(sys.argv[2])