from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

from movies.items import MovieItem, MovieLoader

import re
import sys

class MovieSpider(Spider):
    name = "movie_spider"
    allowed_domains = ["http://www.rottentomatoes.com/"]
    start_urls = ["http://www.rottentomatoes.com/top/bestofrt/?category=1"]

    def parse(self, response):

        try:
            sel = Selector(response)

            # not sure if this needs editing
            movies = sel.xpath('//table[@class="left rt_table"]/tbody/tr')

            # make sure we have a list of movies
            if not movies:
                self.log("Unable to find list of movies in {:s}.".format(response.request.url), level=log.ERROR)

            items = []

            for movie in movies:
                # Ignore the header row, which is the first row returned
                if (movie.xpath('th')):
                    continue

                loader = ItemLoader(MovieItem(), response = response, selector = movie)

                loader.add_xpath('rank', 'td[1]/text()', re = r'\d+') # ignore the '.'
                loader.add_xpath('rating', 'td[2]/span/span[2]/text()', re = r'\d+')
                loader.add_xpath('title', 'td[3]/a/text()' ) #, re = r'.*(?= \([0-9]{4}\))')
                loader.add_xpath('review_count', 'td[4]/text()')
                loader.add_xpath('year', 'td[3]/a/text()', re = r'\d{4}(?=\)$)')

                yield loader.load_item()

        except Exception as e:
            # Log the exception then reraise it.
            self.log("Could not parse URL '{:s}'".format(response.request.url), level=log.ERROR)

