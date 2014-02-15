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

    # needs category
    category     = Field()   # Movie's category (action, adventure, etc)
    
    # Ratings for MPAA, sex, violence, language, etc.
    rating_mpaa  = Field()   # R, PG-13, etc.
    rating_sex   = Field()   # How high it scores on sexuality   
    rating_violence = Field() # How violent the movie is 
    rating_language = Field() # How bad it is as far as language goes
    rating_tomatoes = Field() # The rating on Rotten Tomatoes

    rank         = Field()   # Ranking on RottenTomatoes
    title        = Field()
    review_count = Field()   # How many reviews are on RottenTomatoes.
    year         = Field()   # The year it was made

    details_href = Field()   # Address to the page with further details
    
class MovieLoader(ItemLoader):

    default_item_class = MovieItem()



