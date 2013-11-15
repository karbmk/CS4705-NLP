__author__="Emily Schultz <ess2183@columbia.edu>"
__date__="$Nov 15, 2013"

import sys
import pickle
import collections
from collections import defaultdict

"""
The first part of Question 5 of HW3: Run the IBM Model 2 for 5 iterations on
the pair of English and German files.
"""

def ibm2(english_file, german_file, iterations=5):
    """Run the IBM Model 2 for 5 iterations."""

    # INITIALIZATION STEP
    # get the previously saved t parameters from file
    with open('t_parameters', 'rb') as handle:
        t = pickle.load(handle)
    print "t parameters successfully loaded from pickle file."

    # create empty dictionary for q parameters
    q = defaultdict(dict)

    # open the input files
    en_infile  = open(english_file, 'r')
    ger_infile = open(german_file, 'r')
    
    # get each line of the german and english files
    for en_line in en_infile:
        ger_line = ger_infile.readline()

        # split the lines
        en_split  = en_line.split()
        ger_split = ger_line.split()

        # intialize the q(j|i,l,m) = 1\(l+1)
        total_align = len(en_split) + 1
        for l in range(0, len(en_split) + 1):
            for m in range(0, len(ger_split)):
                q[(len(en_split), len(ger_split))][(l, m+1)] = 1.0/total_align
    
    # close files
    en_infile.close()
    ger_infile.close()

    print "t & q initialized, now performing iterations"
    # IBM 2 ALGORITHM
    # (default 5) iterations
    for it in range(0, iterations):
        print "ITERATION %d" %it
        # open the input files
        en_infile  = open(english_file, 'r')
        ger_infile = open(german_file, 'r')

        # empty count dicts
        en_counts  = defaultdict(int)
        ger_counts = defaultdict(int)
        m_counts  = defaultdict(int)
        l_counts = defaultdict(int)

        # get each line of the german and english files
        for en_line in en_infile:
            ger_line = ger_infile.readline()

            # split the lines
            en_split  = en_line.split()
            ger_split = ger_line.split()            

            # iterate through german word index
            for m in range(0, len(ger_split)):
                ger_word = ger_split[m]
                
                # iterate through english words, increasing total
                total = q[(len(en_split),len(ger_split))][(0, m+1)] * t['NULL'][ger_word]
                for l in range(0, len(en_split)):
                    total += q[(len(en_split),len(ger_split))][(l+1, m+1)] * t[en_split[l]][ger_word]

                # iterate through english word index
                for l in range(0, len(en_split)+1):
                    # TADA: logic here
                    if l == 0:
                        en_word = 'NULL'
                    else:
                        en_word = en_split[l-1]

                    # calculate delta value
                    delta = t[en_word][ger_word] * q[(len(en_split), len(ger_split))][(l, m+1)]/float(total)
                    
                    # increment all counts by delta
                    en_counts[en_word] += delta
                    ger_counts[(ger_word, en_word)] += delta
                    m_counts[(m+1, len(en_split), len(ger_split))] += delta
                    l_counts[(l+1, m+1, len(en_split), len(ger_split))] += delta

        # close the files
        en_infile.close()
        ger_infile.close()

        # update the t parameters
        for en_word in t.iterkeys():
            for ger_word in t[en_word].iterkeys():
                t[en_word][ger_word] = ger_counts[(ger_word, en_word)]/float(en_counts[en_word])

        # update the q parameters
        for j in (q[(len(en_split), len(ger_split))]).iterkeys():
            q[(len(en_split), len(ger_split))][j] = l_counts[(j[0], j[1], len(en_split), len(ger_split))]/float(m_counts[(j[1], len(en_split), len(ger_split))])

    print "iteration complete - outputting t and q parameters to file"
    
    # output the t parameters to the file "t_parameters_2"
    with open("t_parameters_2", 'wb') as handle:
        pickle.dump(t, handle)

    # output the q parameters to the file "q_parameters"
    with open("q_parameters", 'wb') as handle:
        pickle.dump(q, handle)

def usage():
    print """
    python ibm2.py [english_file] [german_file]
        Generates t and q parameters by performing 5 iterations of the IBM Model 2,
        and outputs to the file "t_parameters_2"
    """

if __name__ == "__main__":
    # expect exactly two arguments: the english file and the german file
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    ibm2(sys.argv[1], sys.argv[2])
