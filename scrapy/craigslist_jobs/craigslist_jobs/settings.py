# Scrapy settings for craigslist_jobs project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'craigslist_jobs'

SPIDER_MODULES = ['craigslist_jobs.spiders']
NEWSPIDER_MODULE = 'craigslist_jobs.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'craigslist_jobs (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
     'craigslist_jobs.pipelines.CraigslistJobsPipeline'
]
