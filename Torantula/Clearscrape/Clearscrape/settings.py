# -*- coding: utf-8 -*-

# Scrapy settings for Clearscrape project
# Adapted directly from Torantula Settings
BOT_NAME = 'Clearscrape'

SPIDER_MODULES = ['Clearscrape.spiders']
NEWSPIDER_MODULE = 'Clearscrape.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

############################################################################
# ----------------------------SCRAPY SPEED SETTINGS -------------------------
############################################################################

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 120  # was 32

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 15  # was 32, then 64

# Configure a delay for requests for the same website (default: 0)
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1  # was 0.5

# Reduce download timeout so stuck requests discarded quickly. default 180
DOWNLOAD_TIMEOUT = 60

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.75

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 3
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

############################################################################
# ----------------------------END SPEED SETTINGS -------------------------
############################################################################

############################################################################
# ----------------------------CRAWL BEHAVIOR -------------------------------
############################################################################

# No more than 2 links deep on every site
DEPTH_LIMIT = 2

# Prioritize DFS or BFS. 1=BFS
DEPTH_PRIORITY = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Retry connections after connection failure
RETRY_ENABLED = False

# Allow sites to redirect the scraper
REDIRECT_ENABLED = False

############################################################################
# ----------------------------END CRAWL BEHAVIOR -------------------------
############################################################################

SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

AJAXCRAWL_ENABLED = True

# Allocate more system resources? See scrapy broad crawls documentation
REACTOR_THREADPOOL_MAXSIZE = 20

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True
TELNETCONSOLE_PORT = [6023]

# Additional built-in depth middleware.
SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 290,
}

# Enable or disable extensions
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': 420,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'Clearscrape.pipelines.PagetextPipeline': 300,
    # 'Clearscrape.pipelines.MySQLPipeline': 310
}

# Randomized from this list for each page access
USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0'
]

# Each of these are in middlewares.py
DOWNLOADER_MIDDLEWARES = {
    'Clearscrape.middlewares.IgnoreDomainMiddleware': 390,
    'Clearscrape.middlewares.RandomUserAgentMiddleware': 410,
    'Clearscrape.middlewares.ProxyMiddleware': 400,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 430
}

# Privoxy server is a SOCKS proxy (to talk to Tor) but acts as an HTTP proxy for Clearscrape.
#HTTP_PROXY = 'http://localhost:8118'

# tail -f --retry ScrapyResults.txt to view the logfile in realtime
LOG_FILE = '/tmp/ScrapyResults.txt'

# 'DEBUG' for more information, such as what links are being ignored due to depth
LOG_LEVEL = 'INFO'
