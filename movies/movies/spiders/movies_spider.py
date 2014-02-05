from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

from movies.items import MovieItem
from movies.items import MovieLoader

class MovieSpider(Spider):
   name = "movie_spider"
   allowed_domains = ["http://www.rottentomatoes.com/"]
   start_urls = ["http://www.rottentomatoes.com/top/bestofrt/?category=1"]

   def parse(self, response):
      sel = Selector(response)

      # not sure if this needs editing
      movies = sel.xpath('//table[@class="left rt_table"]/tbody/tr')
      
      items = []

      for movie in movies:
         # create a new movie record
         #loader = MovieLoader(item = MovieItem(), response = response)

         item = MovieItem()

         # clean up the '.' at the end of the ranking
         # get the ranking from the page, remove the '.', and convert to ascii
         #loader.add_xpath('rank', 'td[1]/text()')
         #loader.add_xpath('rating', 'td[2]/span/span[2]/text()')
         #loader.add_xpath('title', 'td[3]/a/text()')
         #loader.add_xpath('review_count', 'td[4]/text()')

         item['rank']   = movie.xpath('td[1]/text()').extract()
         item['rating'] = movie.xpath('td[2]/span/span[2]/text()').extract()
         item['title']  = movie.xpath('td[3]/a/text()').extract()
         item['review_count'] = movie.xpath('td[4]/text()').extract()
            
         items.append(item)
         # don't forget the year
         # item['year'] = ...

      return items

# I learned that when you output a file when running scrapy,
# it just appends to the file instead of overwriting it. I had the correct output
# only it was way down in the file and I was seeing the old, buggy output on top