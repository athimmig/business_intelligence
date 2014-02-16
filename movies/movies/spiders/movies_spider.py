# encoding=utf-8
from scrapy import log
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request # for processing details

from movies.items import MovieItem, MovieLoader

import re
import sys

class MovieSpider(Spider):
    name = "movie_spider"
    allowed_domains = ["rottentomatoes.com"]
    start_urls = ["http://www.rottentomatoes.com/top/bestofrt/?category=1"]

    ''' Additional pages:
                    "http://www.rottentomatoes.com/top/bestofrt/?category=2",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=3",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=4",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=5",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=6",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=7",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=8",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=9",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=10",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=11",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=12",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=13",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=14",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=15",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=16",
                    "http://www.rottentomatoes.com/top/bestofrt/?category=17",'''

    def __init__(self):
        self.item_loader_buffer = {}

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

                # Gather information about the movie
                loader = ItemLoader(MovieItem(), response = response, selector = movie)

                # Generate the href for the details page
                details_href = 'http://' + response.url.split('/')[2] + str(movie.xpath('td[3]/a/@href').extract()[0])

                loader.add_xpath('category', '//form[@action="/top/bestofrt/"]/p/select/option[@selected="selected"]/text()')

                loader.add_xpath('rank', 'td[1]/text()', re = r'\d+') # ignore the '.'
                loader.add_xpath('rating_tomatoes', 'td[2]/span/span[2]/text()', re = r'\d+')
                loader.add_xpath('title', 'td[3]/a/text()', re = r'.*(?= \([0-9]{4}\))')
                loader.add_xpath('review_count', 'td[4]/text()')
                loader.add_xpath('year', 'td[3]/a/text()', re = r'\d{4}(?=\)$)')

                # Store the item loader into the temporary buffer while we step away from the function
                self.item_loader_buffer[details_href] = loader

                try:
                    # Request additional information on the movie
                    print "Requesting additional information at %s" % details_href
                    yield Request(url=details_href, callback=self.parse_movie_details)
                except Exception as e:
                    print e

                # Load the item 
                yield loader.load_item()

        except Exception as e:
            print "Error: ", e
            # log("Could not parse URL '{:s}'".format(response.request.url), level=log.ERROR)

    def parse_movie_details(self, response):
        # Process further details here
        print response
        # Rating xpath: sel.xpath('//span[@itemprop="contentRating"]/text()').extract()

        return None

