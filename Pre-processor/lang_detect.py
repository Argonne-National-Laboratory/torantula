import nltk
from nltk.corpus import stopwords
import process_utils as p_utils

#from Alejandro Nolla
#blog.alejandronolla.com/2013/05/15/detecting-text-language-with-python-and-nltk
def detect_lang(input):
    words = [x.lower() for x in input]
    language_ratios = {}
    language_ratios['unknown'] = 5 #min threshold set to account for noise.

    #load arabic and chinese stopwords -- others are included in nltk corpus
    arabic = set(nltk.word_tokenize(open(
    'stop_words/stopwords-ar.txt', 'r').read().decode('utf8')))
    chinese = set(nltk.word_tokenize(open(
    'stop_words/stopwords-zh.txt', 'r').read().decode('utf8')))

    #chinese works best if done by character
    ch_words = p_utils.flatten([list(x) for x in words])

    #check stopwords in each nltk stopword corpus
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        language_ratios[language] = len(common_elements)

    #selects key(language) with highest value from language ratios
    most_common_lang = max(language_ratios, key=language_ratios.get)
    
    return most_common_lang
    #end nolla code
