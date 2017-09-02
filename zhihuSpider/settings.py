# -*- coding: utf-8 -*-

# Scrapy settings for zhihuSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihuSpider'

SPIDER_MODULES = ['zhihuSpider.spiders']
NEWSPIDER_MODULE = 'zhihuSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENTS = ["Mozilla/4.0 (compatible; GoogleToolbar 6.1.1518.856; Windows 6.0; MSIE 7.0.6001.18000)",
              "Mozilla/4.0 (compatible; GoogleToolbar 6.1.1518.856; Windows 6.0; MSIE 8.0.6001.18702)",
              "Mozilla/4.0 (compatible; GoogleToolbar 6.1.1518.856; Windows 6.0; MSIE 8.0.6001.18702)",
              "Mozilla/4.0 (compatible; MSIE 4.01; Windows CE; PPC; MDA compact/3.0 Profile/MIDP-2.0 Configuration/CLDC-1.1)",
              "Mozilla/4.0 (compatible; MSIE 4.01; Windows NT Windows CE)",
              "Mozilla/4.0 (compatible; MSIE 5.0; AOL 8.0; Windows 98; DigExt; FunWebProducts)",
              "Mozilla/4.0 (compatible; MSIE 5.0; Series90/1.1 Nokia7710/4.01.0 Profile/MIDP-2.0 Configuration/CLDC-1.0)"
              "Mozilla/4.0 (compatible; MSIE 5.5; AOL 7.0; Windows 98; PKBL008)"]
RANDOM_UA_TYPE = "random"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# MONGO_URI = 'mongodb://localhost:27017/'
# MONGO_DATABASE='zhihu'

#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'zhihuSpider.middlewares.RandomUserAgent': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihuSpider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'zhihuSpider.pipelines.MysqlTwistedPipline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = "localhost"
MYSQL_DBNAME = "zhihuSpider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "008"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"
