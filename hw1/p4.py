__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Sep 27, 2013"

import sys
from collections import defaultdict
import math
from count_freqs import Hmm

"""
As a baseline, implement a simple named entity tagger that always produces the tag 
y* = argmax(y) e(x|y)
for each word x. Make sure your tagger uses the RARE word probabilities for rare 
and unseen words. Your tagger should read in the counts ﬁle and the ﬁle ner_dev.dat
(which is ner_dev.key without the tags) and produce output in the same format as
the training ﬁle, but with an additional column in the end that contains the 
log probability for each prediction.
"""

def problem4(count_file, dev_file):
    """Implement a simple named entity tagger and output predictions."""

    try:
        input = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Read counts
    counter.read_counts(input)
    # Write the predictions
    counter.write_predicts(counter, dev_file, sys.stdout)

def usage():
    print """
    python p4.py [counts_file] [dev_file] > [prediction_file]
        Read in a counts file and dev input files, and produce output in format:
        word tag log_probability
        to prediction_file.
    """

if __name__ == "__main__":

    # expect exactly two arguments: the counts file and the dev file
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    problem4(sys.argv[1], sys.argv[2])