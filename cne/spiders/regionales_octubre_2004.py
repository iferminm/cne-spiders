#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import Selector

class Regionales2004Spider(BaseSpider):
    name = 'regionales2004'
    allowed_domains = ['cne.gov.ve']
    start_urls = ['http://www.cne.gob.ve/regionales2004/menuXestados.html']

    def parse(self, response):
        sel = Selector(response)
        states = sel.xpath('//td')
        for state in states:
            state_name = state.xpath('a/text()').extract()
            state_link = state.xpath('a/@href').extract()
