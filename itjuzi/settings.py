# -*- coding: utf-8 -*-

# Scrapy settings for itjuzi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'itjuzi'

SPIDER_MODULES = ['itjuzi.spiders']
NEWSPIDER_MODULE = 'itjuzi.spiders'

ITEM_PIPELINES = {
                    'itjuzi.pipelines.ItjuziPipeline' : 1
                 }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "spider"
DB_PSWD = "654321"
DB_NAME = "itjuzi"
