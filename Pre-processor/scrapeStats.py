"""
The scrapeStats class is responsible for encapsulating all the formerly
global variables related to languages statistics across a scrape.
"""

class ScrapeStats:
    '''
    Initializes a scrapestats object with a language dictionary, and array to keep
    count of domains found for each language
    '''
    def __init__(self):
        self.doc_total = 0
        self.lang_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.languages = {"unknown":0, "dutch":1, "english":2, "finnish":3,
        "french":4, "german":5, "hungarian":6, "italian":7, "kazakh":8,
        "norwegian":9, "portuguese":10, "romanian":11, "russian":12, "spanish":13,
        "swedish":14, "turkish":15, "danish":16, "arabic":17, "chinese":18}

# increment total document count
    def increment_total(self):
        self.doc_total += 1

# increment value corresponding to language, lang
    def increment_lang_count(self, lang):
        self.lang_count[self.languages[str(lang)]] += 1

#writes counts of domains found for each language out to a text file
    def write_stats(self, outfile):
        outfile = outfile + 'stats.txt'
        output = open(outfile, 'w')
        output.write('SCRAPE STATISTICS\n')
        output.write('domains scraped: %s\n' %self.doc_total)
        output.write('english domains processed: %s\n' % self.lang_count[2])
        output.write('\nLanguage Statistics\n')
        for lang in self.languages:
            output.write(
            lang + ": %s" % self.lang_count[self.languages[lang]] + '\n')
        output.close()
