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
    sql = "INSERT INTO %s VALUES (%s, %s, %s, %s, %s)" % (MYSQL_TABLE,
          escape_string(movie['rank']),
          escape_string(movie['rating']),
          escape_string(movie['title']),
          escape_string(movie['review_count']),
          escape_string(movie['year']))

    if cursor.execute(sql):
        print "Inserted %s" % movie['title']
    else:
        print "Insertion Error"

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

