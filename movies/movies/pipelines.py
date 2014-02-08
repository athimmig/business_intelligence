# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem

class WriteToJSONPipeline(object):

    # open file
    def __init__(self):
        self.file = open('movies.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

        print "Scraped '{:s}'".format(item['title'])
        
        return item
