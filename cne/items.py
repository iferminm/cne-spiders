#coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

class Common(Item):
    """
    Atributos comunes para identificar
    y asociar otras clases con un determinado
    proceso en cada una de las mesas electorales
    de un centro de votación determinado
    """
    proceso = Field()
    anio = Field()
    estado = Field()
    municipio = Field()
    parroquia = Field()
    centro = Field()
    mesa = Field()


class InformacionMesa(Common):
    """
    Información general de las mesas electorales
    para un proceso dado
    """
    electores = Field()
    electores_en_actas = Field()
    electores_escrutados = Field()
    votos = Field()
    nulos = Field()
    abstencion = Field()
    actas = Field()
    actas_escrutadas = Field()


class ResultadoMesa(Common):
    """
    Resultados asociados a un candidato determinado
    para un cargo de elección popular en cada una de las
    mesas electorales
    """
    candidato = Field()
    cargo = Field()
    votos = Field()
    porcentaje = Field()
    comun = Field()
    ficha_tecnica = Field()
