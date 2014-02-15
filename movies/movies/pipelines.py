# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
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
    rank        = int(movie['rank'][0])
    rating      = int(movie['rating'][0])
    title       = str(movie['title'][0])
    review_count = int(movie['review_count'][0])
    year        = int(movie['year'][0])

    # Change %s to %d where appropriate
    sql = """INSERT INTO %s VALUES 
        (null, %d, %d, \"%s\", %d, %d)""" % (
        MYSQL_TABLE,
        rank, rating, title, review_count, year)

    try:
        cursor.execute(sql)
        connection.commit()
        print "Inserted record for %s" % title

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
        self.json_exporter = JsonLinesItemExporter(open('movies.json', 'wb'))
        self.json_exporter.start_exporting()

        # Since the charts frequently change, we need to deal with differences
        # in the cached data and current data. 
        # For now, we'll just truncate the table when the spider opens
        # and dump everything in.

        cursor = connection.cursor()

        sql = 'truncate table %s' % MYSQL_TABLE

        try:
            cursor.execute(sql)
            connection.commit()
            print "Truncated %s Table" % MYSQL_TABLE
        except:
            print "Error %d %s" % (e.args[0], e.args[1])
            connection.rollback()

    def process_item(self, item, spider):
        # store the item in the database
        insert_database(item)

        # Write to JSON file
        self.json_exporter.export_item(item)

        return item

    def spider_closed(self, spider):
        # signal end of export
        self.json_exporter = finish_exporting()

