# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

from scrapy.contrib.loader.processor import TakeFirst, Join
from scrapy.contrib.loader import ItemLoader

# Item is the base class
# MovieItem is the extended class
# Field is another object

class MovieItem(Item):
   rank     = Field()
   rating   = Field()
   title    = Field()
   review_count = Field()
   
class MovieLoader(ItemLoader):
   rank_in = Join()