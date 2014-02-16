2# Scrapy settings for movies project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import MySQLdb # connect()
import sys # exit()

BOT_NAME        = 'movie_bot'
BOT_VERSIONS    = '0.1'
SPIDER_MODULES  = ['movies.spiders']
NEWSPIDER_MODULE = 'movies.spiders'

MYSQL_DB = 'movies'
MYSQL_TABLE = 'movies'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'cangetin'

# Open spider-database connection
try:
    connection = MySQLdb.connect(host = MYSQL_HOST,
                                user = MYSQL_USER,
                                passwd = MYSQL_PASSWORD,
                                db = MYSQL_DB)
    # Silence is golden.
except MySQLdb.Error, e:
    print "Unable to connect to database."
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

# Politeness
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = .25 # delay 1 second for download times
ROBOTSTXT_OBEY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'movies (+http://www.yourdomain.com)'

# Pipeline
ITEM_PIPELINES = {
    # Lower numbers take greater precedence
    'movies.pipelines.MoviesPipeline': 0
}

LOG_FILE = 'movies_spider.log'