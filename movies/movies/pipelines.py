# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals, log
from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import JsonLinesItemExporter

from movies.settings import *

from MySQLdb import *

import json
import settings # conn

# Store data in database
def insert_database(movie):
    if not movie: # doubt I really need this, but just in case...
        return

    cursor = connection.cursor()
    
    # Use prepared statements later
    rank = int(movie['rank'][0])
    rating_tomatoes = int(movie['rating_tomatoes'][0])
    title = str(movie['title'][0])
    review_count = int(movie['review_count'][0])
    year = int(movie['year'][0])
    category = str(movie['category'][0])

    # Change %s to %d where appropriate
    sql = """INSERT INTO {:s} 
        (id, rank, rating_tomatoes, title, review_count, year, category)
        VALUES 
        (null, {:d}, {:d}, \"{:s}\", {:d}, {:d}, \"{:s}\")""".format(MYSQL_TABLE,
        rank, rating_tomatoes, title, review_count, year, category)

    # Debug the SQL statement if needed:
    # print sql

    try:
        cursor.execute(sql)
        connection.commit()
        print "Scraped information for %s" % title

    except MySQLdb.Error, e:
        print "Error %d: %s" % ( e.args[0], e.args[1])
        connection.rollback()

# The MoviePipeline
class MoviesPipeline(object):
    
    def __init__(self):
        self.field_to_export = []
        self.file = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # signals start of export

        print "Spider opened...\nPreparing to crawl..."



        # Since the charts frequently change, we need to deal with differences
        # in the cached data and current data. 
        # For now, we'll just truncate the table when the spider opens
        # and dump everything in.

        cursor = connection.cursor()

        sql = 'truncate table %s' % MYSQL_TABLE

        try:
            cursor.execute(sql)
            connection.commit()
            print "*** Truncated %s Table ***" % MYSQL_TABLE
        except:
            print "Error %d %s" % (e.args[0], e.args[1])
            connection.rollback()

    def process_item(self, item, spider):
        # store the item in the database
        insert_database(item)
        return item

    def spider_closed(self, spider):
        # signal end of export
        return None

