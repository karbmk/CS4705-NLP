# Emily Schultz (ess2183)
# COMS 4705
# Question 5

import sys
import subprocess
import string
from collections import defaultdict
from subprocess import PIPE

def call(process, stdin):
    """For use with given processes."""
    output = process.stdin.write(stdin + '\n\n')
    line = ''
    while 1:
        l = process.stdout.readline()
        if not l.strip(): 
            break
        line += l
    return line

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
def get_features(histories, sentence, v, score, f=1):
    scores = ''
    for history in histories: # Iterate through histories
        parsed = str.split(history)
        if len(parsed) > 0 and parsed[2] != 'STOP':
            pos = int(parsed[0])-1
            word = str.split(sentence[pos])[0] # Extract word corresponding to history from sentence
            tag = parsed[2] # Extract tag from history
            weight = 0
            standard = ['BIGRAM:'+parsed[1]+':'+tag, 'TAG:'+word+':'+tag]
            features = features_set(word, tag, standard, f, pos) # Create feature set
            for feature in features:
                # Calculating weight for each history
                # Add all scores of features all features of history in dictionary to weight
                # If feature weight is zero, it might not be in dictionary, but weight does not change anyway
                # If a feature is not used by a model, it will not be in v, and thus will not affect the score
                if score == 1:
                    if feature in v:
                        weight += v[feature]
                # Calculating features for sequence of histories
                # Increment counts of all features of history
                # Used only to train, not to tag
                else:
                    if feature in v:
                        v[feature] += 1
                    else:
                        v[feature] = 1
            scores += (history + ' ' + str(weight) + '\n')
    if score == 1:
        return scores[:-1] # Return scored histories
    return v # Return dictionary of weights

# Train model from 'train' file and write to 'model' file
def train_model(train_file, model_file):
    """Train a model using the train_file, and output it to the model file."""
    # run the given processes
    gold_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'GOLD'], stdin=PIPE, stdout=PIPE)
    enum_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'ENUM'], stdin=PIPE, stdout=PIPE)
    history_server = subprocess.Popen(['python', 'tagger_decoder.py', 'HISTORY'], stdin=PIPE, stdout=PIPE)

    model = defaultdict(int)
    # gold dictionaries
    gold_dict = {}
    gold_tags = {}

    for it in range(0, 5): # Iterations of training algorithm
        i = 0
        train_infile = open(train_file, 'r')

        # read each line of the untagged file
        sentence = ''
        for line in train_infile:

            # get each word in the sentence
            if len(line) > 1:
                sentence += line

            # now we've got the whole sentence
            else:
                sentence = sentence[:-1]
                s = sentence.split('\n')

                # get the gold history on the first time 
                if it == 0:
                    gold = call(gold_server, sentence)
                    gold_tags[i] = gold
                    # get the features
                    gold_dict[i] = get_features(gold.split('\n'), s, {}, 0)

                # get the possible histories
                histories = call(enum_server, sentence).split('\n')
                # get the features for the histories
                scores = get_features(histories, s, model, 1)
                # find the best history
                tags = call(history_server, scores).split('\n')

                # case where best is not a gold
                if tags != gold_tags[i]:
                    features = get_features(tags, s, {}, 0)
                    for feature in (gold_dict[i]).iterkeys():
                        model[feature] += gold_dict[i][feature]
                    for feature in features.iterkeys():
                        model[feature] -= features[feature]
                i += 1
                sentence = ''
        train_infile.close()

    # write the model out to the model file
    outfile = open(model_file, 'w')
    for feature in model.iterkeys():
        outfile.write(feature + ' ' + str(model[feature]) + '\n')
    outfile.close()

    # return the model dictionary
    return model

def usage():
    print """
    python q5.py [train_file] [output_file]
        Uses train_file to train and model and output the model to the output_file.
    """

def main(args):
    # expect exactly two arguments: the training data, and the output filename
    if len(sys.argv) != 3:
        usage()
        sys.exit(2)

    train_model(args[1], args[2])

if __name__ == "__main__":
    main(sys.argv)