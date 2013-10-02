__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Sep 27, 2013"

import sys
from collections import defaultdict
import math
from count_freqs import Hmm

"""
Reads in lines of state trigrams y(i-2), y(i-1), y(i) (separated by space)
and prints out the log probability for each trigram.
"""

def problem5(trigram_file, count_file):
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
    counter.write_trigram_prob(trigram_file, sys.stdout)


def usage():
    print """
    python p5.py [trigram_file] [counts_file] > [prob_file]
        Read in a counts file and trigram input files, and produce output in format:
        (trigram) log_probability
        to prob_file.
    """

if __name__ == "__main__":

    # expect exactly two arguments: the trigram file and the count file
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    problem5(sys.argv[1], sys.argv[2])