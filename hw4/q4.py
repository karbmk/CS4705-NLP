# Emily Schultz, ess2183
# COMS 4705 

import sys
import subprocess, string
from collections import defaultdict
from subprocess import PIPE

def call(process, stdin):
    output = process.stdin.write(stdin + '\n\n')
    line = ''
    while 1:
        l = process.stdout.readline()
        if not l.strip(): break
        line += l
    return line

# Tag untagged file using pre-trained model v; write to tagged file
def pretrained_tag(v, untagged, tagged):
    enum_server = process(['python', 'tagger_history_generator.py', 'ENUM'])
    history_server = process(['python', 'tagger_decoder.py', 'HISTORY'])
    untagged_file = open(untagged, 'r')
    tagged_file = open(tagged, 'w')
    sentence = ''
    for line in untagged_file:
        if len(line) > 1: # Middle of sentence
            sentence += line
        else: # End of sentence
            sentence = sentence[:-1] # Remove trailing newline
            histories = str.split(call(enum_server, sentence), '\n') # Enumerate possible histories for sentence
            sentence = str.split(sentence)
            scores = calc_features(histories, sentence, v, -1) # Calculate weights for all histories
            tags = str.split(call(history_server, scores), '\n') # Find highest scoring sequence of histories
            for i in range(len(sentence)): # Extract tag from each history and write to file
                parsed = str.split(tags[i])
                tagged_file.write(sentence[i] + ' ' + parsed[2] + '\n')
            tagged_file.write('\n')
            sentence = ''
    tagged_file.close()
    untagged_file.close()

# Return set of features for model
# Input f indicates which features to use: 0-BIGRAM, TAG; 1-BIGRAM, TAG, SUFFIX; 2-BIGRAM, TAG, PREFIX; 3-BIGRAM, TAG, SUFFIX, PREFIX; 4-BIGRAM, TAG, LENGTH; 5-BIGRAM, TAG, CASE; 6-BIGRAM, TAG, CASE, SUFFIX; 7-BIGRAM, TAG, CASE, PREFIX
def features_set(word, tag, features, f, i):
    if f in (-1, 1, 3, 6):
        features.extend(['SUFFIX:'+word[-3:]+':3:'+tag, 'SUFFIX:'+word[-2:]+':2:'+tag, 'SUFFIX:'+word[-1:]+':1:'+tag])
    if f in (-1, 2, 3, 7):
        features.extend(['PREFIX:'+word[:3]+':3:'+tag, 'PREFIX:'+word[:2]+':2:'+tag, 'PREFIX:'+word[:1]+':1:'+tag])
    if f in (-1, 4):
        features.append('LEN:'+str(len(word))+':'+tag)
    # Determine case of word
    if f in (-1, 5, 6, 7):
        lo = string.lowercase
        up = string.uppercase
        num = string.digits
        pun = string.punctuation
        for i in range(len(word)):
            if i == 0:
                if string.find(lo, word[i]) != -1:
                    type = 'LO'
                elif string.find(up, word[i]) != -1:
                    type = 'SEN'
                elif string.find(num, word[i]) != -1:
                    type = 'NUM'
                elif string.find(pun, word[i]) != -1:
                    type = 'PUN'
                else:
                    type = 'MIX'
                    break
            else:
                if string.find(lo+pun, word[i]) == -1 and type in ['LO', 'SEN']:
                    type = 'MIX'
                    break
                elif string.find(up+pun, word[i]) == -1 and type == 'UP':
                    type = 'MIX'
                    break
                elif string.find(pun, word[i]) == -1 and type == 'PUN':
                    if string.find(lo, word[i]) != -1:
                        type = 'LO'
                    elif string.find(up, word[i]) != -1:
                        type = 'UP'
                    elif string.find(num, word[i]) != -1:
                        type = 'NUM'
                elif string.find(num+pun, word[i]) == -1 and type == 'NUM':
                    type = 'MIX'
                    break
        features.append('CASE:'+type+':'+tag)
    return features

# Extract features from histories
# Score is indicator for return value
# If score == 1, calculate weight for each history and return string of histories with weights
# If score == 0, return dictionary of features for sequence of histories
def calc_features(histories, sentence, v, f):
    scores = ''
    for history in histories: # Iterate through histories
        parsed = history.split()
        if len(parsed) > 0 and parsed[2] != 'STOP':
            pos = int(parsed[0])-1
            word = sentence[pos].split()[0] # Extract word corresponding to history from sentence
            tag = parsed[2] # Extract tag from history
            weight = 0
            standard = ['BIGRAM:'+parsed[1]+':'+tag, 'TAG:'+word+':'+tag]
            features = features_set(word, tag, standard, f, pos) # Create feature set
            for feature in features:
                # Calculating weight for each history
                # Add all scores of features all features of history in dictionary to weight
                # If feature weight is zero, it might not be in dictionary, but weight does not change anyway
                # If a feature is not used by a model, it will not be in v, and thus will not affect the score
                if feature in v:
                    weight += v[feature]
            scores += (history + ' ' + str(weight) + '\n')
    return scores[:-1] # Return scored histories

def process(args):
    """Calls a script using PIPE from provided script."""
    return subprocess.Popen(args, stdin=PIPE, stdout=PIPE)

def map_model(model_file):
    """Create model dictionary using the model file."""
    infile = open(model_file, 'r')
    model = defaultdict(int)
    for line in infile:
        line_list = line.split()
        model[line_list[0]] = float(line_list[1])
    infile.close()
    return model

def usage():
    print """
    python q4.py [model_file] [untagged_file] [tagged_file]
        Uses model_file to tag the untagged_file and output results to the tagged file.
    """

def main(args):
    # expect exactly three arguments: the model, the dev data, and the output filename
    if len(sys.argv) != 4:
        usage()
        sys.exit(2)

    model = map_model(args[1])
    pretrained_tag(model, args[2], args[3])

if __name__ == "__main__":
    main(sys.argv)