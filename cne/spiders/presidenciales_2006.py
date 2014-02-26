#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from cne.items import Common, InformacionMesa, ResultadoMesa
from scrapy.http.request import Request

class Presidenciales2006(BaseSpider):
    name = 'presidenciales_2006'
    start_urls = [
        'http://www.cne.gob.ve/divulgacionPresidencial/resultado_nacional.php'
    ]

    def parse(self, response):
        selector = Selector(response)
        tables_width_300 = selector.xpath('//table[@width="300"]') # Los estados están en una tabla de estas características
        odd_rows = tables_width_300[1].xpath('.//tr[@bgcolor="#EEEEEE"]')
        even_rows = tables_width_300[1].xpath('.//tr[@bgcolor="#DDDDDD"]')
        
        states = odd_rows.xpath('.//a') + even_rows.xpath('.//a')
        states += tables_width_300[2].xpath('.//tr[@bgcolor="#EEEEEE"]').xpath('.//a')

        for state in states:
            name = state.xpath('.//text()')[0].extract()
            comun = Common(proceso='Presidenciales', anio=2013, estado=name.strip())

            location = state.xpath('.//@href')[0].extract()
            url_tokens = response.url.split('/')
            url_tokens[-1] = location
            url = '/'.join(url_tokens)

            yield Request(url, meta={'common_info': comun}, callback=self.parse_estado)

    def parse_estado(self, response):
        comun = response.meta['common_info']
        selector = Selector(response)
        tables_width_300 = selector.xpath('//table[@width="300"]')
        odd_rows = tables_width_300.xpath('.//tr[@bgcolor="#EEEEEE"]')
        even_rows = tables_width_300.xpath('.//tr[@bgcolor="#DDDDDD"]')
        municipios = odd_rows.xpath('.//a') + even_rows.xpath('.//a')

        for municipio in municipios:
            name = municipio.xpath('.//text()')[0].extract()
            comun['municipio'] = name.strip()
            location = municipio.xpath('.//@href')[0].extract()
            url_tokens = response.url.split('/')
            url_tokens[-1] = location
            url = '/'.join(url_tokens)

            yield Request(url, meta={'common_info': comun}, callback=self.parse_municipio)


    def parse_municipio(self, response):
        return Common()
        #yield Request(url, meta={'common_info': comun}, callback=self.parse_parroquia)

    def parse_parroquia(self, response):
        yield Request(url, meta={'common_info': comun}, callback=self.parse_centro)

    def parse_centro(self, response):
        yield Request(url, meta={'common_info': comun}, callback=self.parse_mesa)

    def parse_mesa(self, response):
        pass
