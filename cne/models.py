from sqlalchemy import create_engine, Column, Integer, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.engine.url import URL

import settings

Base = declarative_base()


def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    Base.metadata.create_all(engine)


class Eleccion(Base):
    __tablename__ = 'eleccion'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(512), nullable=False)
    anio = Column(Integer, nullable=False)


class CentroElectoral(Base):
    __tablename__ = 'centro_electoral'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(512), nullable=False)
    estado = Column(String(128), index=True, nullable=False)
    municipio = Column(String(256), index=True, nullable=False)
    parroquia = Column(String(256), index=True, nullable=False)


class MesaElectoral(Base):
    __tablename__ = 'mesa_electoral'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(16), nullable=False)
    centro_id = Column(Integer, ForeignKey('centro_electoral.id'), index=True, nullable=False)


class InfoMesa(Base):
    __tablename__ = 'info_mesa'

    id = Column(Integer, primary_key=True)
    electores = Column(Integer, nullable=False)
    electores_en_actas = Column(Integer, nullable=False)
    electores_escrutados = Column(Integer, nullable=False)
    votos = Column(Integer, nullable=False)
    nulos = Column(Integer, nullable=False)
    abstencion = Column(Integer, nullable=False)
    actas = Column(Integer, nullable=False)
    actas_escrutadas = Column(Integer, nullable=False)
   
    mesa_id = Column(Integer, ForeignKey('mesa_electoral.id'), index=True, nullable=False)
    mesa = relationship('MesaElectoral', backref=backref('infos', order_by=id))

    eleccion_id = Column(Integer, ForeignKey('eleccion.id'), index=True, nullable=False)
    eleccion = relationship('Eleccion', backref=backref('infos', order_by=id))


class ResultadoMesa(Base):
    __tablename__ = 'resultado_mesa'

    id = Column(Integer, primary_key=True)
    candidato = Column(String(128), index=True)
    cargo = Column(String(128), index=True, nullable=False)
    votos = Column(Integer, nullable=False)
    porcentaje = Column(Integer, nullable=False)


    mesa_id = Column(Integer, ForeignKey('mesa_electoral.id'), index=True, nullable=False)
    mesa = relationship('MesaElectoral', backref=backref('resultados', order_by=id))

    eleccion_id = Column(Integer, ForeignKey('eleccion.id'), index=True, nullable=False)
    eleccion = relationship('Eleccion', backref=backref('resultados', order_by=id))

