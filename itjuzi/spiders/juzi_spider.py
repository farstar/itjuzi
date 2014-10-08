# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.log import INFO, DEBUG, ERROR, WARNING
from itjuzi.items import InvestEventItem

import datetime

class JmspiderSpider(scrapy.Spider):
    name = "juzi-spider"
    allowed_domains = ["itjuzi.com"]
    start_urls = ("http://itjuzi.com/investevents",)

    def __init__(self):
        scrapy.log.start()

    def _get_last_page_seq_id(self, page_links):
      for l in page_links:
        link_texts = l.xpath("./text()").extract()
        if len(link_texts) > 0 and link_texts[0].encode('utf8').find("尾页") >= 0:
          link = l.xpath("./@href").extract()[0].encode('utf8')
          i = link.rfind('=')
          return (link[0 : i + 1], int(link[i + 1 : ]))
      return ("", -1)


    def parse(self, response):
        self.log("enter landing page parser.", DEBUG)
        self.scrap_invest_events(response)

        page_links = response.xpath('//li[@class="page" or @class="next page"]/a')
        link_prefix, last_page_id = self._get_last_page_seq_id(page_links)
        if last_page_id < 0:
          self.log("can not find the last page sequence id.", ERROR)
          return
        self.log("last page sequence id %s" % last_page_id, INFO)
        # the first page is scrapped. so starting from page 2
        for i in range(2, last_page_id + 1):
          yield Request((link_prefix + "%s") % (i) , callback = self.scrap_invest_events)


    def scrap_invest_events(self, response):
        trows = response.xpath('//table[@id="company-member-list"]/tbody/tr')
        self.log("scrap investment event for page %s, %s rows" % (response.url, len(trows)), INFO)
        for r in trows:
          columns = r.xpath("./td")
          if len(columns) < 6:
            self.log("the number of column is less than 6." % columns, ERROR)
            continue

          item = InvestEventItem()

          col_text = columns[0].xpath(".//text()").extract()
          if len(col_text) > 0:
            if col_text[0].encode('utf8').find("时间") >= 0:
              # skip the header row
              continue
            item["e_time"] = col_text[0].encode("utf8").strip()
          else:
            self.log("can not get event time. block: %s" % columns[0], WARNING)
            item["e_time"] = ""

          col_text = columns[1].xpath(".//text()").extract()
          if len(col_text) > 0:
            item["e_corp"] = col_text[0].encode("utf8").strip()
          else:
            self.log("can not get event company. block: %s" % columns[1], WARNING)
            item["e_corp"] = ""

          col_text = columns[2].xpath(".//text()").extract()
          if len(col_text) > 0:
            item["e_round"] = col_text[0].encode("utf8").strip()
          else:
            self.log("can not get event round. block: %s" % columns[2], WARNING)
            item["e_round"] = ""

          col_text = columns[3].xpath(".//text()").extract()
          if len(col_text) > 0:
            item["e_money"] = col_text[0].encode("utf8").strip()
          else:
            self.log("can not get event money. block: %s" % columns[3], WARNING)
            item["e_money"] = ""

          col_text = columns[4].xpath(".//text()").extract()
          if len(col_text) > 0:
            item["e_scope"] = col_text[0].encode("utf8").strip()
          else:
            self.log("can not get event scope. block: %s" % columns[4], WARNING)
            item["e_scope"] = ""

          col_text = columns[5].xpath(".//text()").extract()
          if len(col_text) > 0:
            item["e_invester"] = col_text[0].encode("utf8").strip()
          else:
            self.log("can not get event invester. block: %s" % columns[5], WARNING)
            item["e_invester"] = ""

          yield item

