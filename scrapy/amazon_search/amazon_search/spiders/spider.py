"""Defining the spider to search items from Amazon"""

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from amazon_search.items import AmazonSearchItem
import time
from nltk import clean_html


class ItemSpider(CrawlSpider):
    """The actual spider"""
    name = "amazon_search"
    allowed_domains = ["amazon.com"]
    department = "appliances"
    text = "wine+cooler"

    def build_start_urls(department, text):
        """Build the start URL(s) for the given amazon search.
           Search the specified department for the given text"""
        """This curl command is successful:
        curl -L "http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dappliances&field-keywords=odb+bluetooth+iphone"
        """
        base_str = "http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3D"
        departments = { "books" : "stripbooks",
                        "appliances" : "appliances",
                        "sports & outdoors" : "sporting"
        }
        field_div = "&field-keywords="
        keyword_separator = "+"
        assert department in departments.keys()
        return [base_str + departments[department] +
                field_div + text ]

    def parse_start_url(self, response):
        """Process the entry URL"""
        return self.parse_items(response)

    def parse_items(self, response):
        """Parse the items off the search page"""
        hxs = Selector(response)
        results = []
        items = hxs.xpath("//div[starts-with(@id,'result_')]")
        for item in items:
            time.sleep(.2)
            result = AmazonSearchItem()
            result['full_text'] = item.extract()
            result['item_link'] = item.xpath(".//a/@href").extract()[0]
            results.append(result)
        return results

    start_urls = build_start_urls(department, text)

    
