"""Defining the spider to grab CL jobs from seattle"""

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from craigslist_jobs.items import CraigslistJobsItem
import time
from nltk import clean_html


class JobSpider(CrawlSpider):
    """The actual spicer"""
    name = "craigslist_jobs"
#    allowed_domains = ["craigslist.org","seattle.craigslist.org"]
    start_urls = ["http://seattle.craigslist.org/sof/"]

    extr = (SgmlLinkExtractor(allow=("index\100\.html"),
                              restrict_xpaths=('//a[@class="button next"]',) ))

    rules = (
        Rule(extr,callback='parse_links',follow=True),
       )

    def parse_start_url(self, response):
        """Parse the entry URL"""
        return list(self.parse_links(response))

    def parse_links(self, response):
        """Grab the links off the index page"""
        hxs = Selector(response)
        items = []
        titles = hxs.xpath('//span[@class="pl"]')
        for title in titles:
            time.sleep(.2)
            link = ("http://seattle.craiglist.org" +
                    title.xpath("a/@href").extract()[0])
            item = CraigslistJobsItem()
            item['title'] = title.xpath("a/text()").extract()
            item['int_link'] = link
            request = Request(item['int_link'],callback=self.get_data)
            request.meta['item'] = item
            yield request

    def get_data(self, response):
        """Followed the links grabbed above, and get the full description"""
        hxs = Selector(response)
        item = response.request.meta['item']
        item['text'] = hxs.xpath('//section[@id="postingbody"]').extract()
        item['ext_link'] = hxs.xpath('//section[@id="postingbody"]/a/@href').extract()
        yield item
