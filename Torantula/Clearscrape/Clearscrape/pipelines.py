# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from urlparse import urlparse
import os
import logging
import MySQLdb

from spiders.domaincount import DomainCount
from scrapy.exceptions import DropItem
from parsers import parse_site_components, has_keyword


class PagetextPipeline(object):
    """Every page scraped by the spider is sent here for filtering,
    storage, and parsing.

    A file within /pageTexts is created for each domain, where that domain's
    text contents are stored.
    """

    def __init__(self):
        """Initialize the Pipeline.

        Makes a pageTexts directory, save its file path for later
        Should be .../spiders/pageTexts

        Database connection arguments: host, username, password, database
        """

        try:
            os.chdir('pageTexts')
        except OSError:
            os.mkdir('pageTexts')
            os.chdir('pageTexts')

        newdir = 'scrape_%s' % datetime.now().strftime('%m-%d_%H%M')
        os.mkdir(newdir)
        os.chdir(newdir)
        self.pagetexts = os.getcwd()

    def choose_domain_directory(self, domain):
        """
        A directory for storing text is generated for each domain visited.
        If a domain directory already exists, use that one instead.

        :param domain: The top-level domain (without .com, org, etc.)
        :return: none
        """

        domaindirectory = self.pagetexts + '/%s' % domain
        alldirectories = [x[0] for x in os.walk(self.pagetexts)]

        if domaindirectory not in alldirectories:
            os.mkdir(domain)
            os.chdir(domain)
        else:
            os.chdir(domain)

    def write_text(self, text, url, links):
        """
        Writes the page text to disk in the page's domain-directory.
        Each text file is titled after the complete path sans '/'

        :param text: the UTF-8 encoded text from siteComponents
        :param url: the complete URL of a page
        :param links: the links selected from a page
        :return: The file path to the just-inserted page text
        """

        filename = '%s.txt' % url.path.replace('/', '')
        if filename == '.txt':
            filename = 'main.txt'

        try:
            f = open(filename, 'w')
            f.write(str(text))
            f.close()

            if len(links) > 0:
                if os.path.exists('found_links.txt'):
                    append = 'a'
                else:
                    append = 'w'
                l = open('found_links.txt', append)
                for link in links:
                    l.write(link + '\n')
                l.close()

        except OSError, e:
            logging.info("TEXT WRITE ERROR: %s" % e)

        # filepath = os.getcwd() + '/%s' % filename
        os.chdir(self.pagetexts)
        # return filepath

    def process_item(self, item, spider):
        """
        The function called by the spider for every item scraped.
        Performs a series of parsing and data-storage actions on each item.

        This method is responsible for methods that store page-texts directly
        to disk, and checks if pages contain bad-keyword instances.

        :param item: The Site item passed in by the spider
        :param spider: The current spider performing scraping operations
        :return: the Site item passed by the spider
        """

        # Just in case relocation has not occured
        os.chdir(self.pagetexts)

        text, url, domain, links = parse_site_components(item)

        if spider.dcount.ignore_this(domain):
            raise DropItem("DOWNLOAD FROM: %s" % domain)

        if has_keyword(text):
            spider.dcount.set_ignored_domain(domain)
            raise DropItem("KEYWORD MATCH DETECTED FROM: %s" % domain)

        self.choose_domain_directory(domain)
        #filepath = self.write_text(text, url, links)
        self.write_text(text, url, links)

        return item


class MySQLPipeline(object):
    """
    Pipeline for writing metadata (domain, URL, date accessed) to
    a MySQL database. Not required for the spider to function.
    """

    def __init__(self):

        host, username, password, database
        self.conn = MySQLdb.connect('localhost', 'user', 'password', 'Database')

    def write_db(self, cur, domain, url):
        """
        Writes a page domain, URL, access time, text file_path into the database.
        Rolls back just-completed changes in the event of any errors.

        :param cur: cursor the DB uses to perform operations
        :param domain: the top-level domain of a site,
            (without .com, org, 'asdf1234' from http://asdf1234.com)
        :param item: Site item passed by the spider
        :return: None
        """
        try:
            cur.execute('''
                        insert into pages_visited \
                            (domain, URL, date_accessed)
                        values (%s, %s, %s);
                        ''', [domain, url,
                        datetime.now().strftime('%Y-%m-%d_%H:%M:%S')])

        except MySQLdb.Error, e:
            print "MySQL Error[%d]: %s" % (e.args[0], e.args[1])
            self.conn.rollback()
        self.conn.commit()

    def process_item(self, item, spider):
        """
        The function called by the spider for every item scraped.
        Performs a series of parsing and data-storage actions on each item.

        Here, the item is parsed and the method to write metadata to the
        database is called.

        :param item: The Site item passed in by the spider
        :param spider: The current spider performing scraping operations
        :return: the Site item passed by the spider
        """

        cur = self.conn.cursor()

        text, url, domain, links = parse_site_components(item)
        self.write_db(cur, domain, url)

        return item
