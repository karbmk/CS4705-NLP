#! /usr/bin/python

__author__="Emily Schultz <ess2183@columbia.edu>"
__date__ ="$Oct 25, 2013"

import math
import re
import collections
from collections import defaultdict
import sys

def question4(count_file, tree_file):
    """
    Replace infrequent words (Count(x) < 5) in the original training data file
    with a common symbol _RARE_ and output the new data.
    """
    # open the input files
    count_infile = open(count_file, 'r')
    tree_infile = open(tree_file, 'r')

    # find and replace rare words with _RARE_ keyword
    rare_set = find_rare_words(count_infile)
    replace_rare_words(tree_infile, rare_set)

    # close the input files
    count_infile.close()
    tree_infile.close()

def find_rare_words(count_infile):
    """Return the set of all words that are rare (Count < 5)."""
    # dictionary of word : frequency
    freq_dict = defaultdict(int)

    # iterate through lines of the count_infile to populate the frequency dictionary
    for line in count_infile:
        count_info = line.split()
        # avoid index out of bounds and non-terminals
        if len(count_info) > 3 and count_info[1] == 'UNARYRULE':
            word = count_info[3]
            count = int(count_info[0])
            freq_dict[word] += count

    # set of infrequent words
    rare_set = set()

    # iterate through all keys (words) of the frequency dictionary
    # and add words with Count < 5 to rare_set
    for word in freq_dict.iterkeys():
        if freq_dict[word] < 5:
            rare_set.add(word)
    return rare_set

def replace_rare_words(tree_infile, rare_set):
    """Replace all words in the rare_set with the keyword _RARE_ in the tree."""
    rare_set = map(lambda word : '"' + word + '"]', rare_set)
    whole_tree = tree_infile.read()

    # replace every occurrence of the word with the _RARE_ keyword
    for word in rare_set:
        whole_tree = whole_tree.replace(word, '"_RARE_"]')
    sys.stdout.write(whole_tree)

def usage():
    sys.stderr.write("""
    Usage: python p4.py [count_file] [train_file]
        Print the counts with _RARE_ keyword.\n""")

if __name__ == "__main__":
    # expect exactly two arguments: the counts file and the training data file
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    question4(sys.argv[1], sys.argv[2])
