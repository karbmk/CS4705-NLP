__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Nov 15, 2013"

import sys
import pickle
import collections
from collections import defaultdict

"""
The first part of Question 4 of HW3: Run the IBM Model 1 for 5 iterations on
the pair of English and German files
"""

def ibm1(english_file, german_file, iterations=5):
    """Run the IBM Model 1 for 5 iterations."""

    # INITIALIZATION STEP
    # create empty default dictionaries
    t = defaultdict(dict)
    ger = defaultdict(int)

    # open the input files
    en_infile  = open(english_file, 'r')
    ger_infile = open(german_file, 'r')
    
    # get each line of the german and english files
    for en_line in en_infile:
        ger_line = ger_infile.readline()

        # split the lines
        en_split  = en_line.split()
        ger_split = ger_line.split()

        # iterate through all english/german pairs
        for en_word in en_split:
            for ger_word in ger_split:
                ger[ger_word] = 1
                # all alignments for word pairs, and NULL word too
                t[en_word][ger_word] = 0
                t['NULL'][ger_word]  = 0

    # close files
    en_infile.close()
    ger_infile.close()

    # initialize t(f|e) = 1 / n(e)
    for en_word in t.iterkeys():
        for ger_word in (t[en_word].iterkeys()):
            t[en_word][ger_word] = 1./len(t[en_word])

    # output german words to a file
    with open("german_words", 'wb') as handle:
        pickle.dump(ger, handle)

    print "t initialized, now performing iterations"
    # IBM 1 ALGORITHM
    # (default 5) iterations
    for it in range(0, iterations):
        print "ITERATION %d" %it
        # open the input files
        en_infile  = open(english_file, 'r')
        ger_infile = open(german_file, 'r')

        # empty count dicts
        en_counts  = defaultdict(int)
        ger_counts = defaultdict(int)

        # get each line of the german and english files
        for en_line in en_infile:
            ger_line = ger_infile.readline()

            # split the lines
            en_split  = en_line.split()
            ger_split = ger_line.split()            

            # iterate through german words
            for ger_word in ger_split:# iterate through english words, increasing total
                # iterate through english words, increasing total
                total = t['NULL'][ger_word]
                for en_word in en_split:
                    total += t[en_word][ger_word]

                # TADA: these delta loops aren't equivalent (why?)
                for l in range(len(en_split)+1):
                    if l == 0:
                        en_word = 'NULL'
                    else:
                        en_word = en_split[l-1]
                    # Calculate delta value and increment counts
                    delta = t[en_word][ger_word]/total
                    en_counts[en_word] += delta
                    ger_counts[(ger_word, en_word)] += delta

                # # delta calculation:
                # # NULL first
                # delta = t['NULL'][ger_word]/float(total)
                # en_counts[en_word] += delta
                # ger_counts[(ger_word, en_word)] += delta
                # # iterate through english words
                # for en_word in en_split:
                #     delta = t[en_word][ger_word]/float(total)
                #     en_counts[en_word] += delta
                #     ger_counts[(ger_word, en_word)] += delta

        # close the files
        en_infile.close()
        ger_infile.close()

        # update the t parameters
        for en_word in t.iterkeys():
            for ger_word in t[en_word].iterkeys():
                t[en_word][ger_word] = ger_counts[(ger_word, en_word)]/float(en_counts[en_word])

    print "iteration complete - outputting t parameters to file \"t_parameters\""
    
    # output the t parameters to the file "t_parameters"
    with open("t_parameters", 'wb') as handle:
        pickle.dump(t, handle)

def usage():
    print """
    python ibm1.py [english_file] [german_file]
        Generates t parameters by performing 5 iterations of the IBM Model 1,
        and outputs to the file "t_parameters"
    """

if __name__ == "__main__":
    # expect exactly two arguments: the english file and the german file
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    ibm1(sys.argv[1], sys.argv[2])
