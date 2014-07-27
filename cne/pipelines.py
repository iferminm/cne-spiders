# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from sqlalchemy import sessionmaker
from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


class SaveResultsPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        common_info = item['comun']
        table_info = item['ficha_tecnica']

        election = self._get_election(common_info)
        center = self._get_center(common_info)
        table = self._get_table(center, common_info['mesa'])

        self._set_table_info(table_info, election, center, table)
        self._set_table_result(item, election, table)

        return item

    def _set_table_info(self, info, election, center, table):
        table_info = InfoMesa(
                electores=int(info['electores']),
                electores_en_actas=int(info['electores_en_actas']),
                electores_escrutados=int(info['electores_escrutados']),
                abstencion=int(info['electores_en_actas']) - int(info['electores_escrutados']),
                votos=int(info['votos']),
                nulos=int(info['nulos']),
                actas=int(info['actas']),
                actas_escrutadas=int(info['actas_escrutadas']),
                mesa_id=table.id,
                eleccion_id=election.id
            )
        self.session.add(table_info)
        self.session.commit()

    def _set_table_result(self, item, election, table):
        candidate = item['candidato'].lower()
        votes = int(item['votos'])
        percentage = float(item['porcentaje'][:-1].replace(',', '.'))
        position = item['cargo'].lower()

        table_result = ResultadoMesa(
                candidato=candidate,
                votos=votes,
                porcentaje=percentage,
                cargo=position,
                eleccion_id=election.id,
                mesa_id=table.id
            )
        self.session.add(table_result)
        self.session.commit()

    def _get_election(self, common_info):
        electoral_process = common_info['proceso'].lower()
        year = int(common_info['anio'])
        try:
            election = self.session.query(Eleccion).filter(
                    Eleccion.nombre == electoral_process,
                    Eleccion.anio == year
                ).one()
        except NoResultFound:
            election = Eleccion(nombre=electoral_process, anio=year)
            self.session.add(election)
            self.session.commit()

        return election

    def _get_center(self, common_info):
        state = common_info['estado'].lower()
        municipality = common_info['municipio'].lower()
        sector = common_info['parroquia'].lower()
        center_name = common_info['centro'].lower()

        try:
            center = self.session.query(CentroElectoral).filter(
                    CentroElectoral.nombre == center_name,
                    CentroElectoral.municipio == municipality,
                    CentroElectoral.parroquia == sector, 
                    CentroElectoral.estado == state
                ).one()
        except NoResultFound:
            center = CentroElectoral(
                    nombre=center_name,
                    municipio=municipality,
                    parroquia=sector,
                    estado=state
                )
            self.session.add(center)
            self.session.commit()

        return center

    def _get_table(self, center, name):
        name = name.lower()

        try:
            table = self.session.query(MesaElectoral).filter(
                    MesaElectoral.centro_id == center.id,
                    MesaElectoral.nombre == name
                ).one()
        except NoResultFound:
            table = MesaElectoral(
                    nombre=name,
                    centro_id=center.id
                )
            self.session.add(table)
            self.session.commit()

        return table

