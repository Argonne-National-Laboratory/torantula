README for Tor_Scrape pre-processor.
Written by Joshua McGiff

#   Purpose:

  The purpose of this program is to process raw HTML gathered by the scraper
  and prepare it for use in machine learning models. To this end, the pre-processor
  does the following:

    - strip HTML tags and meta-data --returns only page text.
    - Remove all Javascript elements.
    - Tokenize input text
    - Filter out stopwords with nltk stopword corpus.
    - Lemmatize words to common roots.
    - Write processed text to specified output directory.

#### Language Detection:
An additional feature that has been implemented is language
detection. Our processor it not equipped to handle other the vocabulary and
variable char_sets of alternate languages so only English content is fully
processed and passed on for machine learning. Statistics on languages found while
processing are recorded and written to the /stats directory within our output dir.

#### Dependencies:
    - Natural Language Tool Kit (nltk)
    - BeautifuSoup4 (bs4)
    - lxml

#  Implementation:
##    Arguments:
      This pre-processor has been designed to work with the included spider. As
      such it expects the top-most directory of a given scrape's output as its
      first parameter (see spider README for output format).  The desired output
      directory should be supplied as a second argument. This directory will be
      created at the programs execution.

##    Execution:
###      Init:
        At runtime the program will first initialize it's stopword lists and
        initialize a scrapeStats object to record some statistical elements about
        our scrape. Finally we ensure directories for processed text and stats
        are created.

###      concat:
        our concat functions iterate through files in each domain directory and
        strip out HTML and Javascript. These results are then appended to a text
        file containing all text from a given domain: "'domain_name'-all.txt".  

###      Process:
        Next we iterate through each full_text file stored in the /full_texts
        directory. For each of these files perform language determination and
        only continue processing for those found to be in English. For these remaning
        files we extract stopwords from the text and apply a lemmatizer before writing
        out to the specified output directory.
