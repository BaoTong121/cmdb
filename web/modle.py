from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy import create_engine, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from web import config
import json
from cmdb.type import get_instance


Base = declarative_base()

class Schema(Base):
    __tablename__ = "schema"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False, unique=True)
    desc = Column(String(128), nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)

    fields = relationship('Field')


class Reference:
    def __init__(self, ref: dict):
        self.schema = ref['schema']
        self.field = ref['field']
        self.on_delete = ref.get('on_delete', 'disable')
        self.on_update = ref.get('on_update', 'disable')


class FieldMeta:
    def __init__(self, metastr:str):
        meta = json.loads(metastr)
        if isinstance(meta, str):
            self.instance = get_instance(meta['type'])
        else:
            option = meta['type'].get('option')
            if option:
                self.instance = get_instance(meta['type']['name'], **option)
            else:
                self.instance = get_instance(meta['name'])
        self.unique = meta.get('unique', False)
        self.nullable = meta.get('nullable', True)
        self.default = meta.get('default')
        self.multi = meta.get('multi', False)

        ref = meta.get('reference')
        if ref:
            self.reference = Reference(ref)
        else:
            self.reference = None


class Field(Base):
    __tablename__ = "field"
    __table_args__ = (UniqueConstraint('schema_id', 'name'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False, unique=False)
    meta = Column(Text, nullable=True)
    schema_id = Column(Integer, ForeignKey('schema.id'), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    ref_id = Column(Integer, ForeignKey('field.id'), nullable=True)

    schema = relationship('Schema')
    ref = relationship('Field', uselist=False)

    @property
    def meta_data(self):
        return FieldMeta(self.meta)


class Entity(Base):
    __tablename__ = "entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(48), nullable=False)
    schema_id = Column(Integer, ForeignKey('schema.id'), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    schema = relationship('Schema')

class Value(Base):
    __tablename__ = "value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Text, nullable=True)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    entity_id = Column(Integer, ForeignKey('entity.id'), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

    field = relationship('Field')
    entity = relationship('Entity')


engine = create_engine(config.URL, echo=config.DATABASE_DEBUG)
def creat_all():
    Base.metadata.create_all(engine)

def drop_all():
    Base.metadata.drop_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# drop_all()
# creat_all()
