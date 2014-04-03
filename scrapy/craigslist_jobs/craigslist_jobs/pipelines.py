# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""Pipeline that stores the items in sqlite file"""


from scrapy.http import Request
from scrapy.http import Response
from scrapy.selector import Selector
from craigslist_jobs.items import CraigslistJobsItem
import sqlite3
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from nltk import clean_html


engine = create_engine('sqlite:///seattle_craigslist_jobs.db', echo=False)
Base = declarative_base()

class Job(Base):
    """The jobs database"""
    __tablename__ = "jobs"

    title = Column(String)
    description = Column(String)
    internal_link = Column(String, primary_key=True)
    external_link_1 = Column(String)
    external_link_2 = Column(String)

    def __init__(self, title, desc, ilink, elink1, elink2):
        """Creates a Job object"""
        self.title = title
        self.description = desc
        self.internal_link = ilink
        self.external_link_1 = elink1
        self.external_link_2 = elink2


class CraigslistJobsPipeline(object):
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
        title = str(item['title'][0])
        int_link = str(item['int_link'])
        if len(item['ext_link'])>0:
            ext_link_1 = str(item['ext_link'][0])
        else:
            ext_link_1 = "NULL"
        if len(item['ext_link'])>1:
            ext_link_2 = str(item['ext_link'][1])
        else:
            ext_link_2 = "NULL"
        desc = clean_html(str(item['text'][0].encode('ascii','ignore')))
        new_job = Job(title, desc, int_link, ext_link_1, ext_link_2)
        self.session.add(new_job)
        return item
