__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Nov 15, 2013"

import sys
import pickle
import collections
from collections import defaultdict

"""
The second part of Question 4 of HW3: 
for each English word e in devwords.txt, print the list of the 10 foreign
words with the highest t(f|e) parameter (and the parameter itself).
"""

def top10(dev_file, top=10):
    """Calculate the 10 foreign words with the highest t(f|e)."""

    # get the previously saved t parameters from file
    with open('t_parameters', 'rb') as handle:
        t = pickle.load(handle)
    print "t parameters successfully loaded from pickle file."

    # open the input file and the output file
    dev_infile = open(dev_file, 'r')
    dev_outfile = open("devwords_top10.txt", 'w')

    # iterate through the english words in the dev_file
    for line in dev_infile:
        en_word = line.split()[0]
        dev_outfile.write('English Word: %s;\nGerman Words:\n' %en_word)

        # get german words/probabilities in descending order
        ger_words = sorted(t[en_word], key=(t[en_word]).get, reverse=True)
        ger_probs = sorted((t[en_word]).values(), reverse=True)

        # output the top 10 german words by probability
        for i in range(0, top):
            dev_outfile.write("%s\t%f\n" %(ger_words[i], ger_probs[i]))
        dev_outfile.write("\n")

    # close the input and output files
    dev_infile.close()
    dev_outfile.close()

def usage():
    print """
    python top10.py [words_file]
        For each English word e in devwords.txt, print the list of the 10 German
        words with the highest t(f|e) parameter (and the parameter itself)
        to the file "devwords_top10.txt".
    """

if __name__ == "__main__":
    # expect exactly one arguments: the file of English words
    if len(sys.argv) != 2:
        usage()
        sys.exit(2)
    #translations(sys.argv[1])
    top10(sys.argv[1])
