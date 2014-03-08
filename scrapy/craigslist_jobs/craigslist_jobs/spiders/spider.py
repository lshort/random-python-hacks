from scrapy.spider import Spider
from scrapy.selector import Selector
from craigslist_jobs.items import CraigslistJobsItem

class JobSpider(Spider):
    name = "craiglist_jobs"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://seattle.craigslist.org/sof/"]

    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.xpath("//span[@class='pl']")
        items = []
        for title in titles:
            item = CraigslistJobItem()
            item['title'] = titles.xpath("a/text()").extract()
            item['link'] = titles.xpath("a/@href").extract()
            items.append(item)
        return items
