__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Sep 27, 2013"

import sys
from collections import defaultdict
import math
from count_freqs_6 import Hmm

"""
Same as p4.py, except this time _NUM_ and _CAP_ are implemented in addition to _RARE_.
"""

def problem6(count_file, dev_file):
    """Implement a simple named entity tagger and output predictions."""

    try:
        infile = file(count_file,"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Read counts
    counter.read_counts(infile)
    # Write the predictions
    counter.write_predicts(dev_file, sys.stdout)


def usage():
    print """
    python p6.py [counts_file] [dev_file] > [prediction_file]
        Read in a counts file and dev input files, and produce output in format:
        word tag log_probability
        to prediction_file.
    """

if __name__ == "__main__":

    # expect exactly two arguments: the counts file and the dev file
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    problem6(sys.argv[1], sys.argv[2])