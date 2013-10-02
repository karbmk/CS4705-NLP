#! /usr/bin/python

__author__="Daniel Bauer <bauer@cs.columbia.edu> & Emily Schultz <ess2183@columbia.edu"
__date__ ="$Sep 28, 2013"

import sys
from collections import defaultdict
import math

"""
Count n-gram frequencies in a CoNLL NER data file and write counts to
stdout. 
"""

def simple_conll_corpus_iterator(corpus_file):
    """
    Get an iterator object over the corpus file. The elements of the
    iterator contain (word, ne_tag) tuples. Blank lines, indicating
    sentence boundaries return (None, None).
    """
    l = corpus_file.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            # Extract information from line.
            # Each line has the format
            # word pos_tag phrase_tag ne_tag
            fields = line.split(" ")
            ne_tag = fields[-1]
            #phrase_tag = fields[-2] #Unused
            #pos_tag = fields[-3] #Unused
            word = " ".join(fields[:-1])
            yield word, ne_tag
        else: # Empty line
            yield (None, None)                        
        l = corpus_file.readline()

def sentence_iterator(corpus_iterator):
    """
    Return an iterator object that yields one sentence at a time.
    Sentences are represented as lists of (word, ne_tag) tuples.
    """
    current_sentence = [] #Buffer for the current sentence
    for l in corpus_iterator:        
            if l==(None, None):
                if current_sentence:  #Reached the end of a sentence
                    yield current_sentence
                    current_sentence = [] #Reset buffer
                else: # Got empty input stream
                    sys.stderr.write("WARNING: Got empty input file/stream.\n")
                    raise StopIteration
            else:
                current_sentence.append(l) #Add token to the buffer

    if current_sentence: # If the last line was blank, we're done
        yield current_sentence  #Otherwise when there is no more token
                                # in the stream return the last sentence.

def get_ngrams(sent_iterator, n):
    """
    Get a generator that returns n-grams over the entire corpus,
    respecting sentence boundaries and inserting boundary tokens.
    Sent_iterator is a generator object whose elements are lists
    of tokens.
    """
    for sent in sent_iterator:
         #Add boundary symbols to the sentence
         w_boundary = (n-1) * [(None, "*")]
         w_boundary.extend(sent)
         w_boundary.append((None, "STOP"))
         #Then extract n-grams
         ngrams = (tuple(w_boundary[i:i+n]) for i in xrange(len(w_boundary)-n+1))
         for n_gram in ngrams: #Return one n-gram at a time
            yield n_gram        


class Hmm(object):
    """
    Stores counts for n-grams and emissions. 
    """

    def __init__(self, n=3):
        assert n>=2, "Expecting n>=2."
        self.n = n
        self.emission_counts = defaultdict(int)
        self.ngram_counts = [defaultdict(int) for i in xrange(self.n)]
        self.tag_counts = defaultdict(int) # for simple tagger
        self.word_counts = defaultdict(int)
        self.all_states = set()
        self.all_tags = defaultdict(list) # for viterbi
        self.pi_dict = dict([((0, '*', '*'), 1)]) # initialization step of viterbi

    def train(self, corpus_file):
        """
        Count n-gram frequencies and emission probabilities from a corpus file.
        """
        ngram_iterator = \
            get_ngrams(sentence_iterator(simple_conll_corpus_iterator(corpus_file)), self.n)

        for ngram in ngram_iterator:
            #Sanity check: n-gram we get from the corpus stream needs to have the right length
            assert len(ngram) == self.n, "ngram in stream is %i, expected %i" % (len(ngram, self.n))

            tagsonly = tuple([ne_tag for word, ne_tag in ngram]) #retrieve only the tags            
            for i in xrange(2, self.n+1): #Count NE-tag 2-grams..n-grams
                self.ngram_counts[i-1][tagsonly[-i:]] += 1
            
            if ngram[-1][0] is not None: # If this is not the last word in a sentence
                self.ngram_counts[0][tagsonly[-1:]] += 1 # count 1-gram
                self.emission_counts[ngram[-1]] += 1 # and emission frequencies

            # Need to count a single n-1-gram of sentence start symbols per sentence
            if ngram[-2][0] is None: # this is the first n-gram in a sentence
                self.ngram_counts[self.n - 2][tuple((self.n - 1) * ["*"])] += 1

        # add tag counts
        for word, ne_tag in self.emission_counts:
            self.tag_counts[ne_tag] += self.emission_counts[(word, ne_tag)]


    def write_counts(self, output, printngrams=[1,2,3]):
        """
        Writes counts to the output file object.
        Format:

        """
        # First write counts for emissions
        for word, ne_tag in self.emission_counts:            
            output.write("%i WORDTAG %s %s\n" % (self.emission_counts[(word, ne_tag)], ne_tag, word))


        # Then write counts for all ngrams
        for n in printngrams:            
            for ngram in self.ngram_counts[n-1]:
                ngramstr = " ".join(ngram)
                output.write("%i %i-GRAM %s\n" %(self.ngram_counts[n-1][ngram], n, ngramstr))

    def write_predicts(self, dev_file, output):
        """Writes to output in: (word tag log_probability) format."""
        dev_infile = file(dev_file, "r")

        for line in dev_infile:
            word = line.strip()
            if word: # Nonempty line
                if self.word_counts[word] >= 5:
                    tag = self.simple_named_entity_tagger(word)
                    lprob = math.log(self.e(word, tag))
                else:
                    tag = self.simple_named_entity_tagger("_RARE_")
                    lprob = math.log(self.e("_RARE_", tag))
                output.write("%s %s %f\n" %(word, tag, lprob))
            else: # for matchup with eval script
                output.write("\n")

    def e(self, x, y):
        """
        Computes emission parameters
        e(x|y) = Count(y -> x)/Count(y)
        """
        if x == '*' and y == '*':
            return 1.0
        elif self.tag_counts[y] != 0:
            return self.emission_counts[(x, y)]/float(self.tag_counts[y])
        else:
            return 0.0 # avoid division by zero error if tag_count is zero

    def simple_named_entity_tagger(self, word_x):
        """Returns the tag y* = argmax(y) e(x|y) for every word x."""

        tag = "ERROR: NO BEST TAG FOUND" # if no tag found, uh-oh
        prob = 0.0
        for y in self.all_states:
            cur_prob = self.e(word_x, y)
            if cur_prob > prob:
                tag = y
                prob = cur_prob
        return tag

    def read_counts(self, corpusfile):

        self.n = 3
        self.emission_counts = defaultdict(int)
        self.ngram_counts = [defaultdict(int) for i in xrange(self.n)]
        self.all_states = set()
        self.all_words = set()

        for line in corpusfile:
            parts = line.strip().split(" ")
            count = float(parts[0])
            if parts[1] == "WORDTAG":
                ne_tag = parts[2]
                word = parts[3]
                self.emission_counts[(word, ne_tag)] = count
                self.all_states.add(ne_tag)
                self.all_words.add(word)
                self.tag_counts[ne_tag] += count 
                self.word_counts[word] += 1
                self.all_tags[word].append(ne_tag)
            elif parts[1].endswith("GRAM"):
                n = int(parts[1].replace("-GRAM",""))
                ngram = tuple(parts[2:])
                self.ngram_counts[n-1][ngram] = count

        self.all_tags['*'] = '*'
                
    def q(self, y0, y1, y2):
        """
        Computes parameters
        q(y2|y0,y1) = count(y0, y1, y2)/count(y0, y2)
        for a given trigram y0 y1 y2.
        """
        if self.ngram_counts[1][(y0, y1)] != 0:
            return self.ngram_counts[2][(y0, y1, y2)]/self.ngram_counts[1][(y0, y1)]
        else:
            return 0.0 # avoid division by zero error

    def write_trigram_prob(self, tri_file, output):
        """
        Reads in lines of state trigrams y(i-2) y(i-1) y(i) (separated by space)
        and prints the log probability for each trigram.
        """
        tri_infile = file(tri_file, "r")
        l = tri_infile.readline()
        while l:
            line = l.strip()
            if line: # Nonempty line
                # Extract information from line.
                # Each line has the format
                # y(i-2) y(i-1) y(i)
                fields = line.split(" ")
                prob = math.log(self.q(fields[0], fields[1], fields[2]))
                output.write("%s %s %s %f\n" %(fields[0], fields[1], fields[2], prob))
            else: # Empty line
                output.write("\n")
            l = tri_infile.readline()

    def pi(self, k, u, v, sent):
        """For Viterbi algorithm, pi function"""
        if k == 0 and u == '*' and v == '*':
            return 1
        elif (k, u, v) in self.pi_dict:
            return self.pi_dict[(k, u, v)]
        else:
            prob = 0
            for tag in self.all_tags[sent[k - 2]]:
                cur_prob = self.pi(k - 1, tag, u, sent) * self.q(tag, u, v) * self.e(sent[k], v)
                if cur_prob > prob:
                    prob = cur_prob
            self.pi_dict[(k, u, v)] = prob
            return prob

    def bp(self, k, u, v, sent):
        """For Viterbi algorithm with backpointers, bp function"""
        prob = 0.0
        tag = 'ERROR: TAG NOT FOUND'
        
        for w in self.all_tags[sent[k - 2]]:
            cur_prob = self.pi(k - 1, w, u, sent) * self.q(w, u, v) * self.e(sent[k], v)
            if cur_prob > prob:
                prob = cur_prob
                tag = w
        return tag

    def viterbi_read(self, dev_file):
        """For Viterbi algorithm, writes to output in: (word tag log_probability) format."""
        sent = list('*')
        vsent = list('*')
        dev_infile = file(dev_file, "r")
        l = dev_infile.readline()
        while l:
            word = l.strip()
            if word: # Nonempty line
                sent.append(word)
                if self.word_counts[word] < 5: # still do _RARE_
                    vsent.append("_RARE_")
                else:
                    vsent.append(word)
            else:
                vsent.append('*')
                sent.append('*')
                vresults = self.viterbi(vsent)
                for i in range(1, len(vsent) - 1): # avoid */STOP symbols
                    print "%s %s %f" %(sent[i], vresults[i], math.log(self.pi_dict[i, vresults[i - 1], vresults[i]]))
                print '\n'
                # move on to the next
                self.pi_dict.clear()
                sent = list('*')
                vsent = list('*')
            l = dev_infile.readline()

    def viterbi(self, sent):
        slen = len(sent) - 2     # -2 because we added two * strings
        for k in range(1, slen + 1):
            for u in self.all_tags[sent[k - 1]]:
                for v in self.all_tags[sent[k]]:
                    self.pi(k, u, v, sent)
                    prob = self.pi_dict[(k, u, v)]

        prob = 0
        u_tag = "ERROR: NO TAG FOUND"
        v_tag = "ERROR: NO TAG FOUND"
        for u in self.all_tags[sent[k - 1]]:
            for v in self.all_tags[sent[k]]:
                p = self.pi_dict[(slen, u, v)]
                t = self.q(u, v, "STOP")
                cur_prob = self.pi_dict[(slen, u, v)] * self.q(u, v, "STOP")
                if cur_prob > prob:
                    prob = cur_prob
                    u_tag = u
                    v_tag = v

        trigram = {slen - 1: u_tag, slen: v_tag, 0: '*'}
        for k in range(slen - 2, 0, -1):
            trigram[k] = self.bp(k + 2, trigram[k + 1], trigram[k + 2], sent)

        return trigram



def usage():
    print """
    python count_freqs.py [input_file] > [output_file]
        Read in a named entity tagged training input file and produce counts.
    """

if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        input = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Collect counts
    counter.train(input)
    # Write the counts
    counter.write_counts(sys.stdout)
