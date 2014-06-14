# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""Pipeline that stores the items in sqlite file"""


from scrapy.http import Request
from scrapy.http import Response
from scrapy.selector import Selector
from amazon_search.items import AmazonSearchItem
import sqlite3
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from nltk import clean_html

engine = create_engine('sqlite:///amazon_search_results.db', echo=False)
Base = declarative_base()

class Result(Base):
    """The search results database"""
    __tablename__ = "items"

    full_text = Column(String, primary_key=True)
    title = Column(String)
    stars = Column(String)
    page_no = Column(String)
    rank_in_page = Column(String)
    department = Column(String)
    result_count = Column(String)
    first_result_this_page = Column(String)
    item_link = Column(String)


    def __init__(self, ft, t, s, pn, rip, d, rc, frtp, il ):
        """Creates a Job object"""
        self.full_text = ft
        self.title = t
        self.stars = s
        self.page_no = pn
        self.rank_in_page = rip
        self.department = d
        self.result_count = rc
        self.first_result_this_page = frtp
        self.item_link = il


class AmazonSearchPipeline(object):
    def open_spider(self, spider):
        """Opens the database"""
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        """Commits the changes (no database close needed)"""
        self.session.commit()

    def process_item(self, item, spider):
        """Puts an item into the database, and returns the original item"""
        title = ""
        full_text = str(item['full_text'])
        stars = ""
        page_no = ""
        rank_in_page = ""
        department = ""
        result_count = ""
        first_result_this_page = ""
        item_link = str(item['item_link'])
        print item_link[:20], full_text[:30]
        new_job = Result(full_text, title, stars, page_no,
                      rank_in_page, department, result_count,
                      first_result_this_page, item_link )
        self.session.add(new_job)
        return item


