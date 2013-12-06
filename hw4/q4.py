# Emily Schultz, ess2183
# COMS 4705
# Q4

import sys
import subprocess
import string
from collections import defaultdict
from subprocess import PIPE

def assign_tags(model, untagged_file, output_file):
    """Assign tags to the untagged file using the model, and write out."""
    # run the given processes
    enum_server = subprocess.Popen(['python', 'tagger_history_generator.py', 'ENUM'], stdin=PIPE, stdout=PIPE)
    history_server = subprocess.Popen(['python', 'tagger_decoder.py', 'HISTORY'], stdin=PIPE, stdout=PIPE)
    # open the files
    untag_infile = open(untagged_file, 'r')
    outfile = open(output_file, 'w')
    # read each line of the untagged file
    sentence = ''
    for line in untag_infile:
        # get each word in the sentence
        if len(line) > 1:
            sentence += line
        # now we've got the whole sentence
        else:
            sentence = sentence[:-1]
            # get the possible histories
            histories = call(enum_server, sentence).split('\n')
            sentence = sentence.split()
            scores = get_features(histories, sentence, model)
            # find the best tags
            tags = call(history_server, scores).split('\n')
            # write to the outfile 
            for i in range(0, len(sentence)):
                parsed = tags[i].split()
                outfile.write(sentence[i] + ' ' + parsed[2] + '\n')
            outfile.write('\n')
            # reset the sentence
            sentence = ''
    # close the files
    untag_infile.close()
    outfile.close()

def call(process, stdin):
    """For use with given processes."""
    output = process.stdin.write(stdin + '\n\n')
    line = ''
    while 1:
        l = process.stdout.readline()
        if not l.strip(): break
        line += l
    return line

def get_features(histories, sentence, model):
    """Return scored histories."""
    result = ''
    for history in histories:
        history_list = history.split()
        if history_list and history_list[2] != 'STOP':
            pos = int(history_list[0]) - 1
            # get the word
            word = sentence[pos].split()[0]
            # get the tag
            tag = history_list[2]
            weight = 0
            standard = ['BIGRAM:'+history_list[1]+':'+tag, 'TAG:'+word+':'+tag]
            features = features_set(word, tag, standard)
            # calculate the weight for this history
            for feature in features:
                if feature in model:
                    weight += model[feature]
            result += (history + ' ' + str(weight) + '\n')
    return result[:-1]

def features_set(word, tag, features):
    """Return all model features."""
    # suffixes
    features.extend(['SUFFIX:'+word[-3:]+':3:'+tag, 'SUFFIX:'+word[-2:]+':2:'+tag, 'SUFFIX:'+word[-1:]+':1:'+tag])
    # prefixes
    features.extend(['PREFIX:'+word[:3]+':3:'+tag, 'PREFIX:'+word[:2]+':2:'+tag, 'PREFIX:'+word[:1]+':1:'+tag])
    # length
    features.append('LEN:'+str(len(word))+':'+tag)
    lo = string.lowercase
    up = string.uppercase
    num = string.digits
    pun = string.punctuation
    # find the word case/type
    for i in range(0,len(word)):
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

def map_model(model_file):
    """Create model dictionary using the model file."""
    infile = open(model_file, 'r')
    model = defaultdict(int)
    # read in each line of the file
    for line in infile:
        line_list = line.split()
        # add it to the model
        model[line_list[0]] = float(line_list[1])
    infile.close()
    return model

def usage():
    print """
    python q4.py [model_file] [untagged_file] [output_file]
        Uses model_file to tag the untagged_file and output tags to the output_file.
    """

def main(args):
    # expect exactly three arguments: the model, the dev data, and the output filename
    if len(sys.argv) != 4:
        usage()
        sys.exit(2)

    model = map_model(args[1])
    assign_tags(model, args[2], args[3])

if __name__ == "__main__":
    main(sys.argv)