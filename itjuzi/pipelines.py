# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import scrapy
from scrapy.exceptions import DropItem
from items import InvestEventItem
import settings

class ItjuziPipeline(object):
  def __init__(self):
    self.db_con = MySQLdb.connect(host=settings.DB_HOST, user = settings.DB_USER, passwd = settings.DB_PSWD, db = settings.DB_NAME, port = settings.DB_PORT, charset = "utf8")

  def process_item(self, item, spider):
    item.validate()
    if item.is_scraped(self.db_con):
      raise DropItem("item is scraped.")
    item.save2mysql(self.db_con)
    return item
