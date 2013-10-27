#! /usr/bin/python

__author__="Emily Schultz <ess2183@columbia.edu>"
__date__ ="$Oct 25, 2013"

import math
import re
import collections
from collections import defaultdict
import sys, json

class CKY:
    """Class for the CKY Algorithm."""

    def __init__(self):
        """Create all the empty dicitonaries the CKY algorithm will require."""
        # dictionary of rule counts
        self.rule_dict = defaultdict(int)
        self.rule_dict['UNARY'] = defaultdict(int)
        self.rule_dict['BINARY'] = defaultdict(int)
        self.rule_dict['NONTERMINAL'] = defaultdict(int)

        # dictionary of word counts
        self.word_counts = defaultdict(int)

        # dictionary for maximum likelihood estimate q
        self.q_dict = defaultdict(float)
        self.q_dict['UNARY'] = defaultdict(float)
        self.q_dict['BINARY'] = defaultdict(float)

    def fill_dicts(self, count_infile):
        """Fill dictionary from counts file for unary/binary/nonterminal rules."""
        for line in count_infile:
            line = line.strip()
            line_list = line.split()

            # fill the rule dictionary
            if line_list[1] == "UNARYRULE":
                terminal = line_list[3]
                non_terminal = line_list[2]
                self.rule_dict['UNARY'][(non_terminal, terminal)] += int(line_list[0])
            
                # fill the word count dictionary
                self.word_counts[terminal] += int(line_list[0])

            elif line_list[1] == "NONTERMINAL":
                non_terminal = line_list[2]
                self.rule_dict['NONTERMINAL'][non_terminal] += int(line_list[0])

            elif line_list[1] == 'BINARYRULE':
                non_terminal = line_list[2]
                y = line_list[3]
                z = line_list[4]
                self.rule_dict['BINARY'][(non_terminal, y, z)] += int(line_list[0])
            else:
                sys.stderr.write('Count file invalid format - %s not a valid rule type' %(line_list[1]))
                sys.exit(1)

    def fill_qml_dict(self):
        """Calculates ml for each rule and populates the qml dictionary with probabilities."""
        # go through all unary rules
        for key_tup in self.rule_dict['UNARY'].iterkeys():
            num = self.rule_dict['UNARY'][key_tup]
            denom = self.rule_dict['NONTERMINAL'][key_tup[0]]
            self.q_dict['UNARY'][key_tup] = float(num) / float(denom)

        # go through all binary rules
        for key_tup in self.rule_dict['BINARY'].iterkeys():
            num = self.rule_dict['BINARY'][key_tup]
            denom = self.rule_dict['NONTERMINAL'][key_tup[0]]
            self.q_dict['BINARY'][key_tup] = float(num) / float(denom)

    def cky_alg(self, sentence):
        """Iterative part of cky algorithm for sentence (split into a list of words)."""

        # set up the pi dictionary and backpointer dictionary
        bp_dict = defaultdict()
        pi_dict = defaultdict(float)
        i = 0
        n = len(sentence)
        for word in sentence:
            # check for rare words
            if self.word_counts[word] < 5:
                word = '_RARE_'
                sentence[i] = word
            i += 1
            # iterate through nonterminals to populate the pi dictionary
            for non_terminal in self.rule_dict['NONTERMINAL'].iterkeys():
                # calculate the qml
                pi_dict[(i, i, non_terminal)] = self.q_dict['UNARY'][(non_terminal, word)]

        # loops upon loops for main part of cky
        for l in range(1, n):
            for i in range(1, (n-l + 1)):
                j = i + l
                for x in self.rule_dict['NONTERMINAL'].iterkeys():
                    qmax = 0.0
                    # all matching binary rules with non terminal x
                    r = [(key_tup, qml) for key_tup, qml in self.q_dict['BINARY'].iteritems() if key_tup[0] == x]
                    if len(r) <= 0:
                        pi_dict[(i, j, x)] = 0.0
                        bp_dict[(i, j, x)] = 'e'
                    else:
                        for s in range(i, j):
                            for (key_tup, qml) in r:
                                y = key_tup[1]
                                z = key_tup[2]
                                cur = qml * pi_dict[(i, s, y)] * pi_dict[(s+1, j, z)]
                                if cur > qmax:
                                    qmax = cur
                                    pi_dict[(i, j, x)] = qmax
                                    bp_dict[(i, j, x)] = (s, y, z)

        # get the rules using backpointers
        rules = []
        qkey = 'S'
        # some of the sentences are fragments
        if pi_dict[(1, n, 'S')] == 0.0:
            qmax = 0.0
            for x in self.rule_dict['NONTERMINAL'].iterkeys():
                if pi_dict[(1, n, x)] > qmax:
                    qmax = pi_dict[(1, n, x)]
                    qkey = x
        return self.backp_tree(1, n, qkey, sentence, bp_dict)

    def run_cky(self, tree_infile):
        """Performs the CKY algorithm using the dictionaries of this cky object."""
        for line in tree_infile:
            sys.stderr.write('sentence: %s\n' %(line))
            line = line.strip().split()
            print json.dumps(self.cky_alg(line))

    def backp_tree(self, start, end, non_terminal, sentence, bp_dict):
        """Rebuild the parse tree using backpointers."""
        if start == end:
            return [non_terminal, sentence[start-1]]
        else:
            (s, y, z) = bp_dict[(start, end, non_terminal)]
            return [non_terminal, self.backp_tree(start, s, y, sentence, bp_dict), self.backp_tree(s+1, end, z, sentence, bp_dict)]

def question5(tree_file, count_file):
    """The main method for question 5, running the CKY algorithm."""
    # open the input files
    count_infile = open(count_file, 'r')
    tree_infile = open(tree_file, 'r')

    # create the cky object and fill the dictionary
    q5cky = CKY()
    q5cky.fill_dicts(count_infile)
    q5cky.fill_qml_dict()

    # run the cky algorithm
    q5cky.run_cky(tree_infile)

    # close the input files
    count_infile.close()
    tree_infile.close()

def usage():
    sys.stderr.write("""
    Usage: python cky.py [sentence_file] [counts_file]
        Perform the CKY algorithm on the given sentences using the counts.\n""")

if __name__ == "__main__":
    # expect exactly two arguments: the counts file and the training data file
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    question5(sys.argv[1], sys.argv[2])