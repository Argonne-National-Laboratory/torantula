
'''
THIS IS A TEST FILE -- NOT FOR USE IN PRODUCTION
MAY BE RE-USED IN FUTURE TO HOUSE MISC FUNCTIONS
'''
# -*- coding: utf-8 -*-
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
import time
import glob
import shutil
import sys
import os
import re
from bs4 import BeautifulSoup

languages = {"unknown":0, "dutch":1, "english":2, "finnish":3, "french":4,
"german":5, "hungarian":6, "italian":7, "kazakh":8, "norwegian":9,
"portuguese":10, "romanian":11, "russian":12, "spanish":13, "swedish":14,
"turkish":15, "danish":16, "arabic":17, "chinese":18}
lang_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#retrieves a list of subdirectories in a given top level directory
#this will be pointed at the root dir of a given scan
def get_subdirs(top_level_dir):
    return [dir for dir in os.listdir(top_level_dir)
        if os.path.isdir(os.path.join(top_level_dir, dir))]

#for each directory returned by the above function concat all txt files together
def concat_dir(dir, path):
    outfile = str(path) + '/' + 'full_texts/'+ str(dir) + '-all.txt'
    input_files = str(path) + '/' + str(dir) + '/*.txt'
    filenames = glob.glob(input_files)
    print 'domain_dir: ' + str(dir) + ' filenames: ' + str(filenames) + '\n\n'

    with open(outfile, 'wb') as outfile:
        for filename in filenames:
            if filename == outfile:
                continue
            with open(filename, 'rb') as readfile:
                print  'readfile: ' + str(readfile) + 'outfile:' + str(outfile)
                shutil.copyfileobj(readfile, outfile)


def concat_results(top_level_dir):
    #destination for concatted files
    concat_dest = top_level_dir + '/full_texts/'
    print concat_dest
    if not os.path.exists(concat_dest):
        os.makedirs(concat_dest)
    domains = get_subdirs(top_level_dir)
    print '\n DOMAINS' + str(domains) + '\n'
    for domain in domains:
        if str(domain) != 'full_texts':
            process_dir(domain, top_level_dir)

#****************************************************************
#*********************  Lang Detect *****************************

def strip_html(filepath):
    soup = BeautifulSoup(open(filepath, 'r'), 'lxml').get_text()
    tokens = nltk.word_tokenize(soup)
    print len(tokens)
    return tokens

def flatten(list):
    return [item for sublist in list for item in sublist]

def detect_lang(input):

    words = [x.lower() for x in input]
    language_ratios = {}

    arabic = set(nltk.word_tokenize(open(
    'stop_words/stopwords-ar.txt', 'r').read().decode('utf8')))
    chinese = set(nltk.word_tokenize(open(
    'stop_words/stopwords-zh.txt', 'r').read().decode('utf8')))

    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        language_ratios[language] = len(common_elements)

    language_ratios['arabic'] = len(set(words).intersection(arabic))

    # split characters for chinese Detection
    words2 = [list(x) for x in words]
    words3 = flatten(words2)
    language_ratios['chinese'] = len(set(words3).intersection(chinese))
    print language_ratios



    most_common_lang = max(language_ratios, key=language_ratios.get)
    return most_common_lang







#for testing
def main():
    if sys.argv[1][-1] != '/':
        print "no trailing slash"
        sys.argv[1] = str(sys.argv[1] + '/')
    print sys.argv[1][-1]




if __name__ == "__main__":
    main()
