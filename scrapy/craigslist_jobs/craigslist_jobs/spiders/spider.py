from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from craigslist_jobs.items import CraigslistJobsItem
import time

class JobSpider(CrawlSpider):
    name = "craigslist_jobs"
#    allowed_domains = ["craigslist.org","seattle.craigslist.org"]
    start_urls = ["http://seattle.craigslist.org/sof/"]

    extractor = (SgmlLinkExtractor(allow=("index\100\.html"),
                                   restrict_xpaths=('//a[@class="button next"]',) ))
#    extractor = (SgmlLinkExtractor(allow=("index\100\.html"),
#                                   restrict_xpaths=('//a[@class="button next"]',) ))

    rules = (
        Rule(extractor,callback='parse_links',follow=True),
       )

    def parse_start_url(self, response):
        return list(self.parse_links(response))

    def parse_links(self, response):
        hxs = Selector(response)
        items = []
        titles = hxs.xpath('//span[@class="pl"]')
        for title in titles:
            time.sleep(.1)
            link = ("http://seattle.craiglist.org" +
                    title.xpath("a/@href").extract()[0])
            item = CraigslistJobsItem()
            item['title'] = title.xpath("a/text()").extract()
            item['int_link'] = link
            request = Request(item['int_link'],callback=self.get_data)
            request.meta['item'] = item
            yield request

    def get_data(self, response):
        hxs = Selector(response)
        item = response.request.meta['item']
        item['text'] = hxs.xpath('//section[@id="postingbody"]').extract()
        item['ext_link'] = hxs.xpath('//section[@id="postingbody"]/a/@href').extract()
        yield item
