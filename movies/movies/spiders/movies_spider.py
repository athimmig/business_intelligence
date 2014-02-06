# ISSUES
# * There is an extra "" item in the title list
# * Ratings are split into separate characters
# * Everything is still being output to in array format

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

from movies.items import MovieItem, MovieLoader

import re # RegEx

class MovieSpider(Spider):
    name = "movie_spider"
    allowed_domains = ["http://www.rottentomatoes.com/"]
    start_urls = ["http://www.rottentomatoes.com/top/bestofrt/?category=1"]

    def parse(self, response):
        sel = Selector(response)

        # not sure if this needs editing
        movies = sel.xpath('//table[@class="left rt_table"]/tbody/tr')

        for movie in movies:
            loader = ItemLoader(MovieItem(), response = response, selector = movie)

            loader.add_xpath('rank', 'td[1]/text()', re = r'{d}+') # exclude the '.'
            loader.add_xpath('rating', 'td[2]/span/span[2]/text()', re = r'[^%]')
            loader.add_xpath('title', 'td[3]/a/text()', re = r'.*(?= \([0-9]{4}\))')
            loader.add_xpath('review_count', 'td[4]/text()')
            loader.add_xpath('year', 'td[3]/a/text()', re = r'(?<=\()[0-9]{4}(?=\))')

            yield loader.load_item()

# I learned that when you output a file when running scrapy,
# it just appends to the file instead of overwriting it. I had the correct output
# only it was way down in the file and I was seeing the old, buggy output on top