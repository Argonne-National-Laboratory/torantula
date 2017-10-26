# The Darknet Weathermap Suite

This project contains several tools for scraping a vast amount of web sites and processing the downloaded HTML, with the intention of classifying the crawled domains automatically and eventually generating real-time content reports.

![torantula icon](torantula-icon.png)

**Torantula** is a web-scraper with the capability to crawl through the Tor network and download the HTML and links on each page it visits. Thus, the scraper can collect data from clear-net sites *and* Tor Hidden Services, and should never get banned from sites on either.

The **Pre-Processor** takes an output directory from Torantula as input, concatenates all the text found on a domain together, then performs several formatting and Natural-Language Processing functions on the text, including removing HTML elements and JavaScript, stemming, and language detection.

Finally, the utility within **Grapher** takes an output directory from Torantula as input as well, and generates *.json* and *.gexf* graph files for rendering by by a graphing application

## Requirements

* Python 2.7
* A Ubuntu-based Linux distribution is **HIGHLY RECOMMENDED**

## Examples of usage
### Torantula

Navigate all the way down to the /spiders/ directory from /Torantula/. To run the crawler on a list of sites specified in sites.txt:

`scrapy crawl dark -a sites=sites.txt`

The output will be a /scrape_month-date_time/ directory in Torantula/.../spiders/pageTexts structured as follows:

* scrape_month-date_time
    * randomDomain
        * main.txt
        * login.txt
        * found_links.txt
    * anotherDomain
        * main.txt
        * article.txt
        * found_links.txt
    * yetAnotherDomain...

Read Torantula's log file as a scrape is occuring:

`tail -f --retry /tmp/ScrapyResults.txt`

### Pre-Processor

Within /pre-processor/, run the following on a Torantula output directory:

`python pre-processor.py /pathTo/scrape_month-date_time/ /output/directory/`

The output will be a similar directory structure to that output by the crawler.



### Grapher
Generate domain connectivity graphs in .json and .gexf formats based on the data collected by Torantula for rendering by another application.

`python dataset.py /path/to/scrape_month-date_time/`

The output will be .json and .gexf files in /Grapher/

## Installation

It's **HIGHLY RECOMMENDED** that all python packages be installed in a *virtual environment* [
Python Virtual Environments with virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)

Project Python Packages:

```
pip install scrapy networkx
pip install beautifulsoup4 nltk
```


Database Packages:
```
sudo apt-get install mysql-server && sudo apt-get install libmysqlclient-dev
pip install mysqlclient
```

Tor integration packages:
```
sudo apt-get install privoxy
sudo apt-get install tor
```

There is an easier way to install all necessary Python packages at once. Find pyreqs.txt within the top of the project, and run:

`pip install -r pyreqs.txt`



## Configuration
### Torantula

#### Sites to start scraping:
Torantula will start scraping from a user-defined set of sites but will also scrape from other sites discovered during the crawl. Sites to start scrapes from should be placed within .txt files in Torantula/.../spiders/

#### Ignore Domains:
Torantula automatically filters out requests and responses from encountered top-level domains once they have been visited enough times (defined within Torantula/.../spiders/domaincount.py).

* Any domains you want the spider to automatically ignore can be placed within /spiders/ignoreDomains.txt

#### Bad Keywords:
Torantula will automatically throw out content that contains certain keywords and ignore domains that contain those keywords for the rest of the scraping session.

* place strings that indicate content to be filtered within /spiders/keywords.txt

#### Settings:

Torantula has a vast amount of customizable settings within settings.py
* Within SCRAPY SPEED SETTINGS, download timings and concurrent request parameters can be configured, based on network and system capability.
* Within CRAWL BEHAVIOR, the depth_limit of scrapes can be modified, as well as if the scraper should prioritize depth-first or breadth-first crawls. If you're doing a more focused crawl, retries and redirects can be modified as necessary.

## Tests

#### Grapher

#### Torantula

[find virginia tech steam tunnels site for testing tor integration]

#### Pre-processor

## Package Information

#### Scrapy
The Python framework on which Torantula was built

[Main page](https://scrapy.org/)

[Documentation](https://doc.scrapy.org/en/latest/index.html)

#### Privoxy
The socket proxy which routes Torantula's requests through the Tor network

[Main page](https://www.privoxy.org/)

[Documentation]()

#### Tor
#### Networkx
#### NLTK
#### Beautifulsoup
#### MySQL

## Contributors

Oliver Hui - 2016 - Torantula base design and implementation

Joshua McGiff - 2017 - Pre-processor and data storage/handling

John-Luke Navarro -2017 - Torantula extensive development and data graphing

## License
