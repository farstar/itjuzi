# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.log import INFO, DEBUG, ERROR
from items import InvestEventItem

import datetime

class JmspiderSpider(scrapy.Spider):
    name = "juzi-spider"
    allowed_domains = ["itjuzi.com"]
    start_urls = ("http://itjuzi.com/investevents")

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

        page_links = response.xpath('//li[@class="page" or @class="next page"]/a').extract()
        link_prefix, last_page_id = self._get_last_page_seq_id(page_links)
        if last_page_id < 0:
          self.log("can not find the last page sequence id.", ERROR)
          return
        self.log("last page sequence id %s" % last_page_id, INFO)
        # the first page is scrapped. so starting from page 2
        for i in range(2, last_page_id + 1):
          yield Request((link_prefix + "%s") % (i) , callback = self.scrap_invest_events)


    def scrap_invest_events(self, response):
        trows = response.xpath('//table[@id="company-member-list"]/tbody/tr').extract()
        self.log("scrap investment event for page %s, %s rows" % (len(trows), response.url), INFO)
        for r in trows:
          columns = r.xpath("./th/text()").extract()
          if len(columns) == 0:
            self.log("no table columns", ERROR)
            continue
          # skip the header row
          if columns[0].encode('utf8').find("时间") >= 0:
            continue
          item = InvestEventItem()
          item["e_time"] = columns[0].encode("utf8").strip()
          item["e_corp"] = columns[1].encode("utf8").strip()
          item["e_round"] = columns[2].encode("utf8").strip()
          item["e_money"] = columns[3].encode("utf8").strip()
          item["e_scope"] = columns[4].encode("utf8").strip()
          item["e_invester"] = columns[5].encode("utf8").strip()
          yield item

