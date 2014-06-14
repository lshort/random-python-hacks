# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AmazonSearchItem(Item):
    # define the fields for your item here like:
    # name = Field()
    full_text = Field()
    title = Field()
    stars = Field()
    page_no = Field()
    rank_in_page = Field()
    department = Field()
    result_count = Field()
    first_result_this_page = Field()
    item_link = Field()
    
