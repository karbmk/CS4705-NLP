#! /usr/bin/python

__author__="Emily Schultz <ess2183@columbia.edu>"
__date__ ="$Sep 28, 2013"

import sys
from collections import defaultdict
import math

"""
Read in a named entity tagged training input file, replace any words with a count
less than 5 with the keyword _RARE_, unless they are a numeral (_NUM_) or a Capitalized word (_CAP_) 
and produce counts in moretags_replace.dat file.
"""

def read_and_keywd_replace(fname):
    """
    If Count(word) < 5, replace it with the keyword _RARE_, unless it's a numeral _NUM_ or a capitalized word _CAP_.
    """
    try:
        infile = open(fname, "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    # read in just like in count_freqs.py, calculating counts
    emission_counts = defaultdict(int)

    l = infile.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            # Extract information from line.
            # Each line has the format
            # word pos_tag phrase_tag ne_tag
            fields = line.split(" ")
            emission_counts[fields[0]] += 1                     
        l = infile.readline()

    # create a new output file called rare_replace.dat
    outfile = open("moretags_replace.dat", "w")

    # reopen original file for copying tags, etc.
    infile = open(fname, "r")

    # write out just like in count_freqs.py, but with _RARE_ keyword
    l = infile.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            # Extract information from line.
            # Each line has the format
            # word pos_tag phrase_tag ne_tag
            fields = line.split(" ")
            # Count(x) < 5 -> _RARE_
            if emission_counts[fields[0]] < 5:
                if fields[0].isdigit(): #DIGIT
                    outfile.write("_NUM_ " + fields[1] + '\n')
                elif not fields[0].islower(): #CAPITALIZED
                    outfile.write("_CAP_ " + fields[1] + '\n')
                else: # RARE
                    outfile.write("_RARE_ " + fields[1] + "\n")
            else:
                outfile.write(line + "\n")
        else:
            outfile.write("\n") # for matchup with eval script
        l = infile.readline()
    outfile.close()
    infile.close()

def usage():
    print """
    python count_freqs.py [input_file]
        Read in a named entity tagged training input file, replace any words with a count
        less than 5 with the keyword _RARE_, unless a numeral _NUM_ or capitalized _CAP_,
        and produce counts in moretags_replace.dat
    """

if __name__ == "__main__":

    if len(sys.argv) != 2: # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        input = file(sys.argv[1], "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Read in a named entity tagged training input file, replace and words with a count
    # of less than 5 with the keyword _RARE_ then produce counts in rare_replace.dat file
    read_and_keywd_replace(sys.argv[1])
