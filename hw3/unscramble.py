__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Nov 15, 2013"

import sys
import pickle
import collections
from collections import defaultdict

"""
Question 6 of HW3: 
Print out a new file unscrambled.en that contains the best match from scrambled and original.
"""

def unscramble(english_file, german_file):
    """Find the best match sentence in scrambled for the german file."""

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

    # open the german file, and the output file
    ger_infile = open(german_file, 'r')
    outfile = open('unscrambled.en', 'w')

    # iterate through each german sentence
    for ger_sent in ger_infile: # Iterate over all foreign sentences
        en_file = open(english_file, 'r')

        # find max probability sentence over all english sentences
        max_p = -1.0
        max_sent = ""

        # iterate through the scrambled sentences
        for en_sent in en_file:
            en_split = en_sent.split()
            ger_split = ger_sent.split()

            # get the probability of this alignment
            cur_prob = calc_align_prob(en_sent, ger_sent, t, q, ger)
            if cur_prob > max_p:
                max_p = cur_prob
                max_sent = en_sent

        # write the top sentence to the output file
        outfile.write(str(max_sent))
        en_file.close()

    # close the files
    outfile.close()
    ger_infile.close()

def calc_align_prob(en_sent, ger_sent, t, q, ger):
    """Calculate the probability of the maximum likelihood alignment for the given sentence pair."""
    # split the sentences
    en_split  = en_sent.split()
    ger_split = ger_sent.split()

    # initial probability
    p = 1.0

    # iterate through german sentence indexes
    for ger_i in range(0, len(ger_split)): # Iterate over all foreign sentence positions
        max_prob = 0.0
        max_i = 0

        # do the NULL word first
        if ger_split[ger_i] in t['NULL'] and (len(en_split), len(ger_split)) in q:
            max_prob = float(t['NULL'][ger_split[ger_i]] * q[(len(en_split), len(ger_split))][(0, ger_i + 1)])

        # iterate through english words
        for en_i in range(len(en_split)):
            cur_prob = 0.0

            if en_split[en_i] in t and ger_split[ger_i] in ger:
                if ger_split[ger_i] in t[en_split[en_i]]:
                    cur_prob = t[en_split[en_i]][ger_split[ger_i]]

            # don't go directly to zero, but make it small
            elif en_split[en_i] not in t and ger_split[ger_i] not in ger:
                cur_prob = float(10**-18)
            else:
                cur_prob = float(10**-19)

            # factor in the q prob
            if (len(en_split), len(ger_split)) in q:
                cur_prob = cur_prob * q[(len(en_split), len(ger_split))][(en_i+1, ger_i+1)]
            else:
                cur_prob = 0.0

            # if cur_prob is the new max, update the max
            if cur_prob > max_prob:
                max_i = en_i + 1
                max_prob = float(cur_prob)

        # update the probability based on the most likely
        p = p * max_prob
    return p

def usage():
    print """
    python unscramble.py [scrambled_english_file] [german_file]
        Finds the best sentence match from scrambled_english_file
        and prints to file unscrambled.en
    """

if __name__ == "__main__":
    # expect exactly two arguments: the file of scrambled English words and the German words
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    unscramble(sys.argv[1], sys.argv[2])
