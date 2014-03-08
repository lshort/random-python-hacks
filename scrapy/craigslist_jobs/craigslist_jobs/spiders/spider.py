from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from craigslist_jobs.items import CraigslistJobsItem

class JobSpider(CrawlSpider):
    name = "craigslist_jobs"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://seattle.craigslist.org/sof/"]

    extractor = SgmlLinkExtractor(allow=("index\d00\.html"), restrict_xpaths=('//p[@class="nextpage"]',) )

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
            item = CraigslistJobsItem()
            item['title'] = title.xpath("a/text()").extract()
            item['link'] = title.xpath("a/@href").extract()
            items.append(item)
        return items
