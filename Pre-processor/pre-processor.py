import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import lang_detect as ld
import sys
import os
import process_utils as p_utils
from scrapeStats import ScrapeStats

#TODO: add try/catch blocks where needed
#TODO: add language detection for chinese and arabic - DONE
#TODO: add 'uknown' to language dict for empty sets (currently
#defualting to swedish) -DONE
#TODO: refactor to eliminate/reduce global variable usage -DONE
#TODO: fix output directory naming - DONE
#TODO: seperate modules into seperate files (lang_detect, process, misc) DONE
#TODO: implement "verbose" option for output


'''
********************   NLTK FUNCTIONS ***********************************
'''

#populates the list of stop words to strip from the input text
def get_filter_list():
    stop_words = set(stopwords.words("english"))
    stop_words = [x.encode('utf-8') for x in stop_words]
    filter_words = nltk.word_tokenize(open('filter_words.txt').read().rstrip())
    filter_list = filter_words + stop_words
    return filter_list

#strips out stopwords and most symbols, tokenizes and stems
def process_file(input, output, filter_list, stats):
    filename = input
    output_dir = output
    doc_lang = ''
    stats.increment_total()
    print "filename " + str(filename)

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(open(input, 'r').read().decode('utf8'))

    print tokens[:10]
    doc_lang = ld.detect_lang(tokens)
    stats.increment_lang_count(doc_lang)
    print '\n' + str(doc_lang) + '\n'

    #only attempt to process file for classification if in english
    if str(doc_lang) == 'english':
        t_filtered1 = p_utils.diff(tokens, filter_list)
        text = nltk.Text(t_filtered1)

        #stem words to common roots
        wnl = nltk.WordNetLemmatizer()
        lemma_list = [wnl.lemmatize(t) for t in text]

        #Write resulting data into output file
        outfile = open(str(output_dir) + '/' +str(filename)
        .split(".")[0].split("/")[-1]+'-processed.txt' ,'w')
        for item in lemma_list:
            outfile.write(item.encode('utf8').strip() + ' ')
        outfile.close()
    else:
        return

'''
***************************     MAIN    **************************************
'''

def main():

    if len(sys.argv) < 3:
        print "Error: please specify input and ouput directory\nexiting..."
        sys.exit(1)

    #populates the list of stop words to filter out
    filter_list = get_filter_list()
    #init scrapeStats object
    stats = ScrapeStats()

    #error check for non-existant input directory
    if os.path.isdir(sys.argv[1]):
        full_texts_dir = p_utils.concat_results(sys.argv[1])
    else:
        print "Error: specified input directory does not exist \nexiting..."
        sys.exit(1)

    #fixes naming error if output directory not input with trailing slash
    if sys.argv[2][-1] != '/':
        sys.argv[2] = str(sys.argv[2] + '/')

    #extract name from input directory, crate output dir if not exists already
    scrape_name = str(full_texts_dir).split('/')[-3]
    output_dir = str(sys.argv[2]) + str(scrape_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #create stats directory within output dir for lang stats
    stats_dir = output_dir + '/stats/'
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)

    #iterate through input and process
    for file in os.listdir(full_texts_dir):
        filepath = str(full_texts_dir) + str(file)
        process_file(filepath, output_dir, filter_list, stats)

    #write stats out to file
    stats.write_stats(stats_dir)

    sys.exit(0)

if __name__ == "__main__":
    main()
