import os
import lxml
import glob
from bs4 import BeautifulSoup
'''
#************************************************************************
#***********************   MISC FUNCTIONS *******************************
#************************************************************************
'''

#returns all elements of first list not present in second list
def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

#changes any unicode elements in FreqDist tuples to utf-8
#no longer used since all data is being kept now
def fix_freqDist_encoding(input):
    tupleList = []
    for tuple1 in input[0]:
        if type(tuple1[0]) is unicode:
            tuple1 = ((tuple1[0].encode('utf-8')), tuple1[1])
            tupleList.append(tuple1)
        else:
            tupleList.append(tuple1)
    return tupleList

#for use after string split operations. will re-flatten list
#for example flatten([sample, [word, list]]) -> [sample, word, list]
def flatten(list):
    return [item for sublist in list for item in sublist]

#retrieves a list of subdirectories in a given top level directory
#this will be pointed at the root dir of a given scan
def get_subdirs(top_level_dir):
    return [dir for dir in os.listdir(top_level_dir)
        if os.path.isdir(os.path.join(top_level_dir, dir))]

'''
************************************************************************
************   CONCAT FUNCTIONS    *************************************
************************************************************************
'''

'''
concat_dir will now perform html_text extraction while concatting dir, this
is meant to resolve a bug where BeautifulSoup stops processing at </html> tag
'''
def concat_dir(dir, path):
    outfile = str(path) + '/' + 'full_texts/'+ str(dir) + '-all.txt'
    input_files = str(path) + str(dir) + '/*.txt'
    filenames = glob.glob(input_files)

    with open(outfile, 'wb') as outfile:
        for filename in filenames:
            if filename == outfile:
                continue
            with open(filename, 'rb') as readfile:
                print 'entered readfile: ' + str(filename)
                soup = BeautifulSoup(readfile, 'lxml')
                #remove javascript
                for script in soup(["script", "style"]):
                    script.extract()
                outfile.write(soup.get_text().encode('utf8'))

'''
iterates through the output directory of a scrape
concatenates each individual page to one consolidated page per domain
saves these to a 'full_texts' directory to be processed by the nltk functions
returns filepath to full_text domain files
'''
def concat_results(top_level_dir):
    #destination for concatted files
    concat_dest = top_level_dir + 'full_texts/'
    if not os.path.exists(concat_dest):
        os.makedirs(concat_dest)
    domains = get_subdirs(top_level_dir)
    #print '\n DOMAINS' + str(domains) + '\n'
    for domain in domains:
        if str(domain) != 'full_texts':
            concat_dir(domain, top_level_dir)
#    print 'returning concat dest'
    return concat_dest
