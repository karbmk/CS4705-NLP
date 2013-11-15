__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Nov 15, 2013"

import sys
import pickle
import collections
from collections import defaultdict

"""
The second part of Question 5 of HW3:
Finally use your model to find alignments for the first 20 sentence pairs in the training data.
Print the alignments as a list of m integers containing the ai values to file "align20_2".
"""

def align(english_file, german_file, num=20):
    """Calculate the first 20 sentence pair alignments."""

    # get the previously saved t parameters from file
    with open('t_parameters_2', 'rb') as handle:
        t = pickle.load(handle)
    print "t parameters successfully loaded from pickle file."

    # get the previously saved q parameters from file
    with open('q_parameters', 'rb') as handle:
        q = pickle.load(handle)
    print "q parameters successfully loaded from pickle file."

    # get the previously saved german words from file
    with open("german_words", 'rb') as handle:
        ger = pickle.load(handle)
    print "german words successfully loaded from pickle file."

    # open the corpus infiles and the alignment outfile
    en_file   = open(english_file, 'r')
    ger_file  = open(german_file, 'r')
    align_file = open("align20_2", 'w')

    # first 20 sentences only
    for sent in range(0, num):
        # get english and german sentences
        en_line  = en_file.readline()
        ger_line = ger_file.readline()

        # get the proper alignment for this sentence pair
        alignment = calc_alignment(en_line, ger_line, t, q, ger)

        # print alignment to output file
        align_file.write("%s%s%s\n\n"%(en_line, ger_line, alignment))

    # close the input and output files
    en_file.close()
    ger_file.close()
    align_file.close()

def calc_alignment(en_line, ger_line, t, q, ger):
    """Calculate the maximum likelihood alignment for the given sentence pair."""
    alignment = []

    # split the sentences
    en_split  = str.split(en_line)
    ger_split = str.split(ger_line)
    
    # iterate through german sentence indexes
    for ger_i in range(0, len(ger_split)):

        # find max probability over all english words
        max_prob = 0.0
        max_i = 0

        # NULL first
        if ger_split[ger_i] in t['NULL'] and (len(en_split), len(ger_split)) in q:
            max_prob = t['NULL'][ger_split[ger_i]] * q[(len(en_split), len(ger_split))][(0, ger_i+1)]

        # iterate through english sentence indexes
        for en_i in range(0, len(en_split)):
            cur_prob = 0.0
            if en_split[en_i] in t and ger_split[ger_i] in ger and ger_split[ger_i] in t[en_split[en_i]] and (len(en_split), len(ger_split)) in q:
                cur_prob = t[en_split[en_i]][ger_split[ger_i]] * q[(len(en_split), len(ger_split))][(en_i+1, ger_i+1)]
            
            # if cur_prob is the new max, update the max
            if cur_prob >= max_prob:
                max_prob = cur_prob
                max_i = en_i + 1

        # append the most likely to the alignment
        alignment.append(max_i)
    return alignment

def usage():
    print """
    python align2.py [english_file] [german_file]
        For each of the first 20 sentence pairs in the english_file,
        find alignments and print them to "align20_2".
    """

if __name__ == "__main__":
    # expect exactly two arguments: the english file and the german file
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    align(sys.argv[1], sys.argv[2])
