#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from cne.items import Common, InformacionMesa, ResultadoMesa
from scrapy.http.request import Request

class Presidenciales2013Spider(BaseSpider):
    name = 'presidenciales_2013'
    start_urls = ['http://www.cne.gob.ve/resultado_presidencial_2013/r/1/reg_000000.html?',]

    def parse(self, response):
        selector = Selector(response)
        estados = selector.xpath('//li[@class="region-nav-item"]/a')

        for estado in estados:
            nombre = estado.xpath('text()').extract()[0]
            comun = Common(proceso='Presidenciales', anio=2013, estado=nombre)
            region_code_page = estado.xpath('@href').extract()[0].split('/')[-1]
            url_tokens = response.url.split('/')
            url_tokens[-1] = region_code_page
            url = '/'.join(url_tokens)
            yield Request(url, meta={'common_info': comun}, callback=self.parse_estado)

    def parse_estado(self, response):
        comun = response.meta['common_info']
        selector = Selector(response)
        municipios = selector.xpath('//li[@class="region-nav-item"]/a')

        for municipio in municipios:
            nombre = municipio.xpath('text()').extract()[0]
            comun['municipio'] = nombre
            region_code_page = municipio.xpath('@href').extract()[0].split('/')[-1]
            url_tokens = response.url.split('/')
            url_tokens[-1] = region_code_page
            url = '/'.join(url_tokens)
            yield Request(url, meta={'common_info': comun}, callback=self.parse_municipio)


    def parse_municipio(self, response):
        pass

    def parse_parroquia(self, response):
        pass

    def parse_centro_votacion(self, response):
        pass

    def parse_mesa(self, response):
        pass
