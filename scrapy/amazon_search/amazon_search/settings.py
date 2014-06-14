# Scrapy settings for amazon_search project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lees_amazon_search'

SPIDER_MODULES = ['amazon_search.spiders']
NEWSPIDER_MODULE = 'amazon_search.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'lees_amazon_search (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
     'amazon_search.pipelines.AmazonSearchPipeline'
]
