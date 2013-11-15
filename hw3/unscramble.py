
import sys
import math
import re
import json
import collections
import pickle

# Find most likely alignment for given pair of native and foreign sentences
def alignment_helper(nline, fline, params, foreign_words, model, string):
    a = []
    nparsed = str.split(nline)
    fparsed = str.split(fline)
    flen = len(fparsed)
    nlen = len(nparsed)
    prob = 1.0
    for f in range(flen): # Iterate over all foreign sentence positions
        max_prob = 0.0
        max = 0
        if model == 2 or model == str(2):
            tparams = params[0]
            qparams = params[1]
            lens = (nlen, flen)
            inds = (0, f+1)
            if string == 1:
                lens = str(lens)
                inds = str(inds)
            if fparsed[f] in tparams['NULL'] and lens in qparams:
                max_prob = float(tparams['NULL'][fparsed[f]] * qparams[lens][inds])
        for n in range(nlen): # Iterate over all native sentence positions and find maximum probability alignment
            curr = 0.0
            if nparsed[n] in tparams and fparsed[f] in foreign_words:
                if fparsed[f] in tparams[nparsed[n]]:
                    curr = tparams[nparsed[n]][fparsed[f]]
            elif nparsed[n] not in tparams and fparsed[f] not in foreign_words:
                curr = float(10**-18)
            else:
                curr = float(10**-19)
            if model == 2 or model == str(2):
                lens = (nlen, flen)
                inds = (n+1, f+1)
                if string == 1:
                    lens = str(lens)
                    inds = str(inds)
                if lens in qparams:
                    curr *= qparams[lens][inds]
                else:
                    curr *= 0.0
            if curr > max_prob:
                max = n+1
                max_prob = float(curr)
        prob *= max_prob # Update probability of maximum likelihood alignment
        a.append(max) # Update alignment
    return (a, prob) # Return maximum likelihood alignment and its probability

# Get parameters from files or generate if files do not exist
def parameters(model):
    string = 1

    # get the previously saved t parameters from file
    with open('t_parameters_2', 'rb') as handle:
        tparams = pickle.load(handle)
    print "t parameters successfully loaded from pickle file."

    params = tparams
    if model == 2 or model == str(2):
        # get the previously saved q parameters from file
        with open('q_parameters', 'rb') as handle:
            qparams = pickle.load(handle)
        print "q parameters successfully loaded from pickle file."

        params = (tparams, qparams)
        if tparams is None or qparams is None:
            params = ibm2('corpus.en', 'corpus.de', 5)
            string = 0
    elif tparams is None:
        string = 0
        params = ibm1('corpus.en', 'corpus.de', 5)
    return (params, string)


# Unscramble native alignments
def unscramble(native, foreign):
    temp = parameters(2)
    params = temp[0]
    string = temp[1]
    ffile = open(foreign, 'r')
    afile = open('unscrambled.en', 'w')

    # get the previously saved german words from file
    with open("german_words", 'rb') as handle:
        fwords = pickle.load(handle)
    print "german words successfully loaded from pickle file."

    for fline in ffile: # Iterate over all foreign sentences
        nfile = open(native, 'r')
        max = -1.0
        translation = ''
        for nline in nfile: # Iterate over all native sentences and find maximum likelihood translation
            nparsed = str.split(nline)
            fparsed = str.split(fline)
            flen = len(fparsed)
            nlen = len(nparsed)
            curr = (alignment_helper(nline, fline, params, fwords, 2, 0))[1] # Find probability of maximum likelihood alignment of sentence pair
            if curr > max:
                max = curr
                translation = nline
        afile.write(str(translation)) # Write maximum likelihood translation to output file
        #afile.write(str(max))
        nfile.close()
    afile.close()
    ffile.close()

if __name__ == "__main__":
    # expect exactly two arguments: the file of scrambled English words and the German words
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    unscramble(sys.argv[1], sys.argv[2])

# __author__="Emily Schultz <ess2183@columbia.edu>"
# __date__="$Nov 15, 2013"

# import sys
# import pickle
# import collections
# from collections import defaultdict

# """
# Question 6 of HW3: 
# Print out a new file unscrambled.en that contains the best match from scrambled and original.
# """
# # Unscramble native alignments
# def unscramble(english_file, german_file):

#     # get the previously saved t parameters from file
#     with open('t_parameters_2', 'rb') as handle:
#         t = pickle.load(handle)
#     print "t parameters successfully loaded from pickle file."

#     # get the previously saved q parameters from file
#     with open('q_parameters', 'rb') as handle:
#         q = pickle.load(handle)
#     print "q parameters successfully loaded from pickle file."

#     # get the previously saved german words from file
#     with open("german_words", 'rb') as handle:
#         ger = pickle.load(handle)
#     print "german words successfully loaded from pickle file."

#     ger_infile = open(german_file, 'r')
#     outfile = open('unscrambled.en', 'w')

#     for ger_sent in ger_infile: # Iterate over all foreign sentences
#         en_infile = open(english_file, 'r')
#         max = -1.0
#         translation = ''
#         for nline in en_infile: # Iterate over all native sentences and find maximum likelihood translation
#             en_split = str.split(nline)
#             ger_split = str.split(ger_sent)
#             flen = len(ger_split)
#             nlen = len(en_split)
#             params = (t,q)
#             cur_prob = (calc_align_prob(nline, ger_sent, params, ger, 2))[1] # Find probability of maximum likelihood alignment of sentence pair
#             if cur_prob > max:
#                 max = cur_prob
#                 translation = nline
#         outfile.write(str(translation)) # Write maximum likelihood translation to output file
#         en_infile.close()
#     outfile.close()
#     ger_infile.close()

# def calc_align_prob(nline, ger_sent, params, foreign_words, model):
#     a = []
#     en_split = str.split(nline)
#     ger_split = str.split(ger_sent)
#     flen = len(ger_split)
#     nlen = len(en_split)
#     prob = 1.0
#     for f in range(flen): # Iterate over all foreign sentence positions
#         max_prob = 0.0
#         max_i = 0

#         t = params[0]
#         q = params[1]
#         lens = (nlen, flen)
#         inds = (0, f+1)
#         if ger_split[f] in t['NULL'] and lens in q:
#             max_prob = float(t['NULL'][ger_split[f]] * q[lens][inds])
#         for n in range(nlen): # Iterate over all native sentence positions and find maximum probability alignment
#             cur_prob = 0.0
#             if en_split[n] in t and ger_split[f] in foreign_words and ger_split[f] in t[en_split[n]]:
#                 cur_prob = t[en_split[n]][ger_split[f]]
#             lens = (nlen, flen)
#             inds = (n+1, f+1)
#             if lens in q:
#                 cur_prob *= q[lens][inds]
#             else:
#                 cur_prob *= 0.0
#             if cur_prob > max_prob:
#                 max_i = n+1
#                 max_prob = float(cur_prob)
#         prob *= max_prob # Update probability of maximum likelihood alignment
#         a.append(max_i) # Update alignment
#     return (a, prob) # Return maximum likelihood alignment and its probability





# # def unscramble(english_file, german_file):
# #     """Find the best match sentence in scrambled for the german file."""

# #     # get the previously saved t parameters from file
# #     with open('t_parameters_2', 'rb') as handle:
# #         t = pickle.load(handle)
# #     print "t parameters successfully loaded from pickle file."

# #     # get the previously saved q parameters from file
# #     with open('q_parameters', 'rb') as handle:
# #         q = pickle.load(handle)
# #     print "q parameters successfully loaded from pickle file."

# #     # get the previously saved german words from file
# #     with open("german_words", 'rb') as handle:
# #         ger = pickle.load(handle)
# #     print "german words successfully loaded from pickle file."

# #     # open the german file, and the output file
# #     ger_infile = open(german_file, 'r')
# #     outfile = open("unscrambled.en", 'w')

# #     # iterate through each german sentence
# #     for ger_sent in ger_infile:
# #         # open the english file
# #         en_infile  = open(english_file, 'r')

# #         # find max probability sentence over all english sentences
# #         max_prob = 0.0
# #         max_sent = ""

# #         # iterate through the scrambled sentences
# #         for en_sent in en_infile:
# #             cur_prob = calc_align_prob(en_sent, ger_sent, t, q, ger)
# #             if cur_prob > max_prob:
# #                 max_prob = cur_prob
# #                 max_sent = en_sent
# #         # write the top sentence to the output file
# #         outfile.write(str(max_sent))
# #         en_infile.close()

# #     # close the files
# #     ger_infile.close()
# #     outfile.close()

# # def calc_align_prob(en_line, ger_line, t, q, ger):
# #     """Calculate the maximum likelihood alignment for the given sentence pair."""
# #     # split the sentences
# #     en_split  = str.split(en_line)
# #     ger_split = str.split(ger_line)
    
# #     #probability
# #     p = 1.0

# #     # iterate through german sentence indexes
# #     for ger_i in range(0, len(ger_split)):

# #         # find max probability over all english words
# #         max_prob = 0.0
# #         max_i = 0

# #         # NULL first
# #         if ger_split[ger_i] in t['NULL'] and (len(en_split), len(ger_split)) in q:
# #             max_prob = t['NULL'][ger_split[ger_i]] * q[(len(en_split), len(ger_split))][(0, ger_i+1)]

# #         # iterate through english sentence indexes
# #         for en_i in range(0, len(en_split)):
# #             cur_prob = 0.0
# #             if en_split[en_i] in t and ger_split[ger_i] in ger and ger_split[ger_i] in t[en_split[en_i]] and (len(en_split), len(ger_split)) in q:
# #                 cur_prob = t[en_split[en_i]][ger_split[ger_i]] * q[(len(en_split), len(ger_split))][(0, ger_i+1)]
            
# #             # if cur_prob is the new max, update the max
# #             if cur_prob > max_prob:
# #                 max_prob = cur_prob
# #                 max_i = en_i + 1

# #         # update the probability based on the most likely
# #         p = p * max_prob
# #     return p

# def usage():
#     print """
#     python unscramble.py [scrambled_english_file] [german_file]
#         Finds the best sentence match from scrambled_english_file
#         and prints to file unscrambled.en
#     """


