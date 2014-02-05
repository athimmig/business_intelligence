# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

from scrapy.contrib.loader.processor import TakeFirst, Join
from scrapy.contrib.loader import ItemLoader

from scrapy.contrib.exporter import JsonItemExporter

# Serializers
# TODO: Add text parsing

def serialize_rank(value):
    return str(value)

def serialize_rating(value):
    return str(value)

def serialize_title(value):
    return str(value)

def serialize_review_count(value):
    return str(value)

def serialize_year(value):
    return str(value)

# Item is the base class
# MovieItem is the extended class
# Field is another object
class MovieItem(Item):
   rank     = Field(serializer = serialize_rank)
   rating   = Field(serializer = serialize_rating)
   title    = Field(serializer = serialize_title)
   review_count = Field(serializer = serialize_review_count)
   year     = Field(serializer = serialize_year)
   
class MovieLoader(ItemLoader):
   rank_in = Join()