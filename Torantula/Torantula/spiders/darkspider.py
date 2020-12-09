import logging
import sys

from urlparse import urlparse
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from twisted.internet.error import TimeoutError

from Torantula.items import Site
from domaincount import DomainCount


class DarkSpider(CrawlSpider):
    """
    A web-mining spider.

    The DarkSpider opens a file containing a list of URLs, and crawls through
    each, visiting all domains it discovers while crawling. Any domains that are
    within the ignoreDomains list are disqualified from scraping during the rest
    of the session, although links may still be followed. The DarkSpider
    downloads the full HTML of every page it visits, as well as noting all
    external links on each page.

    To use this spider: scrapy crawl dark -a sites=startingListURLS.txt
    """

    name = 'dark'

    def __init__(self, sites=None, tor=False, db=False, *args, **kwargs):
        """
        Initializes the DarkSpider with a file of sites
        specified from the command line. The user can also indicate if the
        spider should route through Tor, or if the item pipeline should also
        store data in a MySQL database.

        :param sites: A file with a different site to scrape on each line.
        :param args:
        :param kwargs:
        """
        super(DarkSpider, self).__init__(*args, **kwargs)
        try:
            f = open("%s" % sites, "r")
            self.start_urls = [url.strip() for url in f.readlines()]
            f.close()
        except IOError, e:
            print "FILE READ ERROR %s" % e
            sys.exit(1)

        self.tor_activated = bool(tor)
        if db:
            custom_settings = {'ITEM_PIPELINES':
            {
                'Torantula.pipelines.PagetextPipeline': 300,
                'Torantula.pipelines.MySQLPipeline': 310
            }}

    dcount = DomainCount()

    try:
        g = open("ignoreDomains.txt", "r")
        ignoreDomains = [domain.strip() for domain in g.readlines()]
        g.close()
        if len(ignoreDomains) == 0:
            print "ignoreDomains.txt empty. No domains to be ignored initially."

        for domain in ignoreDomains:
            dcount.set_ignored_domain(domain)

    except IOError, e:
        print "No ignoreDomains.txt found. No domains to be ignored initially."

    # The spider follows this rule for each group of links encountered on a page
    rules = (Rule(LxmlLinkExtractor(allow=[r'.+\.(com|org|net|).*'],
                    deny=[r'.+\.(jpg|png|pdf|mp4|mp3|zip| \
                        torrent|mov|gif|txt|csv|webm|epub)'],
                    deny_domains=dcount.get_ignored_domains(),
                    unique=True),
                callback='parse_item',
                process_links='process_links',
                follow=True),)

    def process_links(self, links):
        """
        Called for each list of links collected by the spider.
        Discards those links which have domains in ignoreDomains.

        :param links: A list of scraped Link objects collected by the spider
        :return: a list of Link objects from "good" domains.
        """

        goodlinks = []
        for link in links:
            domain = urlparse(link.url).netloc
            if not self.dcount.ignore_this(domain):
                goodlinks.append(link)

        return goodlinks

    @staticmethod
    def parse_item(response):
        """
        Called by the spider for each response received.
        Defines a Site item based on the URL and
        body text received from each response.

        :param response: Full page response passed by the spider
        :return: A Site item
        """

        item = Site()
        item['url'] = response.url
        item['body'] = response.body
        item['links'] = response.xpath('//a/@href').extract()
        return item

    @staticmethod
    def handle_timeout(failure):
        """
        Logs timeout and other errors
        :param failure: A failure returned by an unsuccessful request
        :return: None
        """

        if failure.check(TimeoutError):
            logging.info("TIMEOUT ON %s" % failure.request)
        else:
            logging.info("ERROR DETECTED: %s" % failure.value)
