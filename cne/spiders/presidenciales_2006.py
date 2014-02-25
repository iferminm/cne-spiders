#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from cne.items import Common, InformacionMesa, ResultadoMesa
from scrapy.http.request import Request

class Presidenciales2013y2012Spider(BaseSpider):
    name = 'presidenciales_2013'
    start_urls = [
            'http://www.cne.gob.ve/divulgacionPresidencial/resultado_nacional.php'
    ]

    def parse(self, response):
        yield Request(url, meta={'common_info': comun}, callback=self.parse_estado)

    def parse_estado(self, response):
        yield Request(url, meta={'common_info': comun}, callback=self.parse_municipio)


    def parse_municipio(self, response):
        yield Request(url, meta={'common_info': comun}, callback=self.parse_parroquia)

    def parse_parroquia(self, response):
        yield Request(url, meta={'common_info': comun}, callback=self.parse_centro)

    def parse_centro(self, response):
        yield Request(url, meta={'common_info': comun}, callback=self.parse_mesa)

    def parse_mesa(self, response):
        pass
