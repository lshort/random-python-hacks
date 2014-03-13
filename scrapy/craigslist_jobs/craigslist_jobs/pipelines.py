# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.http import Request
from scrapy.http import Response
from scrapy.selector import Selector
from craigslist_jobs.items import CraigslistJobsItem
