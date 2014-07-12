from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import ForeignKey, backref

Base = declarative_base()


class Eleccion(Base):
    __table_name__ = 'eleccion'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(512), nullable=False)
    anio = Column(Integer, nullable=False)

    infos = relationship('InfoMesa', order_by='InfoMesa.id', backref='eleccion')
    infos = relationship('ResultadoMesa', order_by='ResultadoMesa.id', backref='eleccion')


class CentroElectoral(Base):
    __table_name__ = 'centro_electoral'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(512), nullable=False)
    estado = Column(String(128), index=True, nullable=False)
    municipio = Column(String(256), index=True, nullable=False)
    parroquia = Column(String(256), index=True, nullable=False)

    mesas = relationship('MesaElectoral', order_by='MesaElectoral.nombre', backref='centro')


class MesaElectoral(Base):
    __table_name__ = 'mesa_electoral'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(16), nullable=False)
    centro_id = Column(Ingeger, ForeignKey('CentroElectoral.id'), index=True, nullable=False)

    centro = relationship('CentroElectoral', backref=backref('mesas', order_by=nombre))
    infos = relationship('InfoMesa', order_by='InfoMesa.id', backref='mesa')
    resultados = relationship('ResultadoMesa', order_by='ResultadoMesa.id', backref='mesa')


class InfoMesa(Base):
    __table_name__ = 'info_mesa'

    id = Column(Integer, primary_key=True)
    electores = Column(Integer, nullable=False)
    electores_en_actas = Column(Integer, nullable=False)
    electores_escrutados = Column(Integer, nullable=False)
    votos = Column(Integer, nullable=False)
    nulos = Column(Integer, nullable=False)
    abstencion = Column(Integer, nullable=False)
    actas = Column(Integer, nullable=False)
    actas_escrutadas = Column(Integer, nullable=False)
   
    mesa_id = Column(Integer, ForeignKey('MesaElectoral.id'), index=True, nullable=True)
    mesa = relationship('MesaElectoral', backref=backref('infos', order_by=id))

    eleccion_id = Column(Integer, ForeignKey('Eleccion.id'), index=True, nullable=True)
    eleccion = relationship('Eleccion', backref=backref('infos', order_by=id))


class ResultadoMesa(Base):
    candidato = Column(String(128), primary_key=True)
    cargo = Column(String(128), index=True, nullable=False)
    votos = Column(Integer, nullable=False)
    porcentaje = Column(Integer, nullable=False)

    mesa_id = Column(Integer, ForeignKey('MesaElectoral.id'), index=True, nullable=True)
    mesa = relationship('MesaElectoral', backref=backref('resultados', order_by=id))

    eleccion_id = Column(Integer, ForeignKey('Eleccion.id'), index=True, nullable=True)
    eleccion = relationship('Eleccion', backref=backref('resultados', order_by=id))
