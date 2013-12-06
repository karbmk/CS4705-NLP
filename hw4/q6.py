# Emily Schultz (ess2183)
# COMS 4705
# Question 6

import sys
import subprocess
import string
from collections import defaultdict
from subprocess import PIPE

def features_set(word, tag, features, feat):
    """Return all model features.
        feat = 'prefix' - prefix id
        feat = 'presuf' - prefix and suffix id
        feat = 'case'   - case of word (lower/upper/number/punctuation/mixed)
        feat = 'len'    - length of word
    """
    if feat == 'presuf':
        # suffixes
        features.extend(['SUFFIX:' + word[-3:] + ':3:' + tag, 'SUFFIX:' + word[-2:] + ':2:' + tag, 'SUFFIX:' + word[-1:] + ':1:' + tag])
    if feat in ['prefix', 'presuf']:
        # prefixes
        features.extend(['PREFIX:' + word[:3] + ':3:' + tag, 'PREFIX:' + word[:2] + ':2:' + tag, 'PREFIX:' + word[:1] + ':1:' + tag])
    if feat == 'len':
        # length
        features.append('LEN:' + str(len(word)) + ':' + tag)
    if feat == 'case':
        # case
        lo = string.lowercase
        up = string.uppercase
        num = string.digits
        pun = string.punctuation

        # find the word case/type
        for i in range(0, len(word)):
            if i == 0:
                if word[i].lower() == word[i]:
                    type = 'LO'
                elif word[i].upper() == word[i]:
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
                    if word[i].lower() == word[i]:
                        type = 'LO'
                    elif word[i].upper() == word[i]:
                        type = 'UP'
                    elif string.find(num, word[i]) != -1:
                        type = 'NUM'
                elif string.find(num+pun, word[i]) == -1 and type == 'NUM':
                    type = 'MIX'
                    break
        # case (lower/upper/number/punctuation/mixed)
        features.append('CASE:'+type+':'+tag)
    return features

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

def get_features(histories, sentence, model, score, feat):
    """Return scored histories, or dictionary of features."""
    result = ''
    for history in histories:
        history_list = history.split()
        if len(history_list) > 0 and history_list[2] != 'STOP':
            pos = int(history_list[0]) - 1
            # get the word and the tag
            word = sentence[pos].split()[0]
            tag = history_list[2]

            weight = 0            
            bigram = 'BIGRAM:' + history_list[1] + ':' + tag
            t = 'TAG:' + word + ':' + tag
            features = features_set(word, tag, [bigram, t], feat)
            
            # calculate the weight for this history
            for feature in features:
                # calculate the weight for this history
                if score == 1:
                    if feature in model:
                        weight += model[feature]
                # for training
                else:
                    if feature in model:
                        model[feature] += 1
                    else:
                        model[feature] = 1
            result += (history + ' ' + str(weight) + '\n')
    if score == 1:
        return result[:-1]
    return model

# Train model from 'train' file and write to 'model' file
def train_model(train_file, model_file, feat):
    """Train a model using the train_file, and output it to the model file."""
    # run the given processes
    gold_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'GOLD'], stdin=PIPE, stdout=PIPE)
    enum_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'ENUM'], stdin=PIPE, stdout=PIPE)
    history_server = subprocess.Popen(['python', 'tagger_decoder.py', 'HISTORY'], stdin=PIPE, stdout=PIPE)

    model = defaultdict(int)
    # gold dictionaries
    gold_dict = {}
    gold_tags = {}

    # iterate for training 5 times
    for it in range(0, 5):
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

                # get the gold history on the first time 
                if it == 0:
                    gold = call(gold_server, sentence)
                    gold_tags[i] = gold
                    # get the features
                    gold_dict[i] = get_features(gold.split('\n'), sentence.split('\n'), {}, 0, feat)

                # get the possible histories
                histories = call(enum_server, sentence).split('\n')
                # get the features for the histories
                scores = get_features(histories, sentence.split('\n'), model, 1, feat)
                # find the best history
                tags = call(history_server, scores).split('\n')

                # case where best is not a gold
                if tags != gold_tags[i]:
                    features = get_features(tags, sentence.split('\n'), {}, 0, feat)
                    for feature in (gold_dict[i]).iterkeys():
                        model[feature] += gold_dict[i][feature]
                    for feature in features.iterkeys():
                        model[feature] -= features[feature]
                i += 1
                # reset the sentence
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
    python q6.py [train_file] [output_file] [feature_keyword]
        Uses train_file to train based on feature_keyword and model and output the model to the output_file.
    """

def main(args):
    # expect exactly three arguments: the training data, the output filename, and the feature name
    if len(sys.argv) != 4:
        usage()
        sys.exit(2)

    train_model(args[1], args[2], args[3])

if __name__ == "__main__":
    main(sys.argv)