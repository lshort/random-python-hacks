# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
"""Data to grab from the craiglist job entry"""


from scrapy.item import Item, Field

class CraigslistJobsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    text = Field()
    title = Field()
    int_link = Field()
    ext_link = Field()
