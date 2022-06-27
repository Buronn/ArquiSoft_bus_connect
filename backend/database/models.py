import json
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=True)
    password = Column(String(256), nullable=False)
    email = Column(String(80), nullable=False)
    phone = Column(String(10), nullable=True)
    fecha_ingreso = Column(Date, nullable=True)
    miembro = relationship('Miembro', back_populates='usuario')
    amistad = relationship('Amistad', back_populates='usuario')
    def __repr__(self):
        return '<Usuario %r>' % self.name

class Amistad(Base):
    __tablename__ = 'amistad'
    usuario_id = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    usuario = relationship('Usuario', back_populates='amistad')
    amigo_id = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Amistad %r>' % self.usuario_id

class Miembro(Base):
    __tablename__ = 'miembro'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey(
        'usuario.id'), nullable=False)
    usuario = relationship('Usuario', back_populates='miembro')
    rol = Column(String(80), nullable=False)
    admin = Column(Boolean, nullable=False)
    publicaciones = relationship(
        'Publicacion', back_populates='miembro', lazy='dynamic')
    join_date = Column(Date, nullable=True)
    grupo_id = Column(Integer, ForeignKey(
        'grupo.id'), nullable=True)
    grupo = relationship('Grupo', back_populates='miembro')
    def __repr__(self):
        return '<Miembro %r>' % self.usuario_id

class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    miembro_id = Column(Integer, ForeignKey(
        'miembro.id'), nullable=False)
    miembro = relationship('Miembro', back_populates='publicaciones')
    titulo = Column(String(80), nullable=False)
    descripcion = Column(String(256), nullable=True)
    create_date = Column(Date, nullable=True)
    def __repr__(self):
        return '<Publicacion %r>' % self.contenido

class Grupo(Base):
    __tablename__ = 'grupo'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(80), nullable=False)
    miembro = relationship('Miembro', back_populates='grupo', lazy=True)

    def __repr__(self):
        return '<Grupo %r>' % self.name


class Evento(Base):
    __tablename__ = 'evento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(256), nullable=False)
    fecha_inicio = Column(String(256), nullable=False)
    fecha_fin = Column(String(256), nullable=False)
    usuario_id = Column(Integer, ForeignKey(
        'usuario.id'), nullable=False)


class LogoutToken(Base):
    __tablename__ = 'logout_token'
    id = Column(Integer, primary_key=True)
    token = Column(String(256), nullable=False)
    date = Column(DateTime, nullable=False)

    def __repr__(self):
        return '<LogoutToken %r>' % self.token


def to_dict(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                # this will fail on non-encodable values, like other classes
                json.dumps(data)
                if data is not None:
                    fields[field] = data
            except TypeError:
                pass
        # a json-encodable dict
        return fields
