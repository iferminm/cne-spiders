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
            region_code_page = estado.xpath('@href').extract()[0].split('/')[2:]
            url_tokens = response.url.split('/')
            url_tokens[-3], url_tokens[-2], url_tokens[-1] = region_code_page
            url = '/'.join(url_tokens)
            yield Request(url, meta={'common_info': comun}, callback=self.parse_estado)

    def parse_estado(self, response):
        comun = response.meta['common_info']
        selector = Selector(response)
        municipios = selector.xpath('//li[@class="region-nav-item"]/a')

        for municipio in municipios:
            nombre = municipio.xpath('text()').extract()[0]
            comun['municipio'] = nombre
            region_code_page = municipio.xpath('@href').extract()[0].split('/')[2:]
            url_tokens = response.url.split('/')
            url_tokens[-3], url_tokens[-2], url_tokens[-1] = region_code_page
            url = '/'.join(url_tokens)
            yield Request(url, meta={'common_info': comun}, callback=self.parse_municipio)


    def parse_municipio(self, response):
        comun = response.meta['common_info']
        selector = Selector(response)
        parroquias = selector.xpath('//li[@class="region-nav-item"]/a')

        for parroquia in parroquias:
            nombre = parroquia.xpath('text()').extract()[0]
            comun['parroquia'] = nombre
            region_code_page = parroquia.xpath('@href').extract()[0].split('/')[2:]
            url_tokens = response.url.split('/')
            url_tokens[-3], url_tokens[-2], url_tokens[-1] = region_code_page
            url = '/'.join(url_tokens)
            yield Request(url, meta={'common_info': comun}, callback=self.parse_parroquia)

    def parse_parroquia(self, response):
        comun = response.meta['common_info']
        selector = Selector(response)
        centros = selector.xpath('//li[@class="region-nav-item"]/a')

        for centro in centros:
            nombre = centro.xpath('text()').extract()[0]
            comun['centro'] = nombre
            region_code_page = centro.xpath('@href').extract()[0].split('/')[2:]
            url_tokens = response.url.split('/')
            url_tokens[-3], url_tokens[-2], url_tokens[-1] = region_code_page
            url = '/'.join(url_tokens)
            yield Request(url, meta={'common_info': comun}, callback=self.parse_centro)

    def parse_centro(self, response):
        comun = response.meta['common_info']
        selector = Selector(response)
        mesas = selector.xpath('//li[@class="region-nav-item"]/a')

        for mesa in mesas:
            nombre = mesa.xpath('text()').extract()[0]
            comun['mesa'] = nombre
            region_code_page = mesa.xpath('@href').extract()[0].split('/')[2:]
            url_tokens = response.url.split('/')
            url_tokens[-3], url_tokens[-2], url_tokens[-1] = region_code_page
            url = '/'.join(url_tokens)
            yield Request(url, meta={'common_info': comun}, callback=self.parse_mesa)


    def parse_mesa(self, response):
        comun = response.meta['common_info']
        selector = Selector(response)

        info = selector.xpath('//div[@id="fichaTecnica"]/table/tr[@class="tblightrow"]')
        mesa_info = InformacionMesa()
        
        mesa_info['electores'] = info[0].xpath('.//td/text()')[-1].extract()
        mesa_info['electores_en_actas'] = info[1].xpath('.//td/text()')[-1].extract()
        mesa_info['electores_escrutados'] = info[2].xpath('.//td/text()')[-1].extract()
        mesa_info['votos'] = info[4].xpath('.//td/text()')[-1].extract()
        mesa_info['nulos'] = info[6].xpath('.//td/text()')[-1].extract()
        mesa_info['actas'] = info[7].xpath('.//td/text()')[-1].extract()
        mesa_info['actas_escrutadas'] = info[8].xpath('.//td/text()')[-1].extract()

        subtotals = selector.xpath('//div[@id="tablaResultados"]/table/tr[@class="tbsubtotalrow"]')

        results = list()
        for subtotal in subtotals:
            row_data = subtotal.xpath('.//td[@class="lightRowContent"]')

            mesa_result = ResultadoMesa()
            mesa_result['candidato'] = row_data[1].xpath('.//a/text()')[0].extract()  # Eliminamos la primera celda porque no nos interesa la foto
            mesa_result['cargo'] = u'Presidente de la República'
            mesa_result['votos'] = row_data[2].xpath('.//span/text()')[0].extract()
            mesa_result['porcentaje'] = row_data[3].xpath('.//span/text()')[0].extract()


            mesa_result['comun'] = [dict(comun)]
            mesa_result['ficha_tecnica'] = [dict(mesa_info)]

            results.append(mesa_result)

        return results
