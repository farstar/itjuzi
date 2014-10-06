# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.exceptions import DropItem

import datetime

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class InvestEventItem(scrapy.Item):
    e_time = scrapy.Field()
    e_invester = scrapy.Field()
    e_money = scrapy.Field()
    e_scope = scrapy.Field()
    e_corp = scrapy.Field()
    e_round = scrapy.Field()

    def validate(self):
      valid = ("e_time" in self) and ("e_invester" in self) and ("e_money" in self) and ("e_scope" in self) and ("e_corp" in self) and ("e_round" in self)
      if not valid:
        raise DropItem("validate Invest event fails.")

    def is_scraped(self, db_connection):
      cur = db_connection.cursor()
      count = cur.execute("SELECT * FROM invest_event WHERE company_name = %s AND round = %s AND scope = %s", (self['e_corp'], self['e_round'], self['e_scope']))
      cur.close()
      return count > 0

    def save2mysql(self, db_connection):
      cur = db_connection.cursor()
      ts = now()
      cur.execute("INSERT INTO invest_event (event_time, invester, company_name, raised_money, round, scope, scraped_time) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self['e_time'], self['e_invester'], self['e_corp'], self['e_money'], self['e_round'], self['e_scope'], ts))
      db_connection.commit()
      cur.close()

