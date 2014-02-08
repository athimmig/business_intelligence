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
    if not movie:
        return

    cursor = connection.cursor()
    
    # Use prepared statements later
    # Major problems with this section.

    # TODO: Convert movie data to proper types
    # Change %s to %d where appropriate
    sql = """INSERT INTO %s VALUES 
        (%s, %s, \"%s\", %s, %s)""" % (
        MYSQL_TABLE,
        movie['rank'],
        movie['rating'],
        movie['title'],
        movie['review_count'],
        movie['year'])

    try:
        cursor.execute(sql)
        connection.commit()
        print "Inserted record for %s" % movie['title']

    except MySQLdb.Error, e:
        print "Error %d: %s", ( e.args[0], e.args[1])
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
        print "EXPORTING"

    def process_item(self, item, spider):
        # store the item in the database
        insert_database(item)

        # Code below will write to file
        #print "Exporting {:s} to JSON".format(item['title'])

        #self.json_exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        # signal end of export
        self.json_exporter = finish_exporting()

