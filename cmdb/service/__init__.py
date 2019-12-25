import math
from web.modle import Schema, Field, Value, Entity, session, FieldMeta
from cmdb.utils import getlogger

logging = getlogger(__name__, 'e:/server.log')


def get_schema_by_name(name:str, deleted:bool=False):
    query = session.query(Schema).filter(Schema.name == name.strip())

    if not deleted:
        query = query.filter(Schema.deleted == False)
    return query.first()


def get_schema_by_id(id:int, deleted:bool=False):
    query = session.query(Schema).filter(Schema.name == id)

    if not deleted:
        query = query.filter(Schema.deleted == False)
    return query.first()


def add_schema(name: str, desc: str=None):
    schema = Schema()
    schema.name = name
    schema.desc = desc
    session.add(schema)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(e)


def delete_schema(id:int):
    try:
        schema = session.query(Schema).filter(Schema.id == id)
        if schema:
            schema.deleted = True
            session.add()
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        else:
            raise ValueError()
    except Exception as e:
        logging.error("fail to del a schema.id = {}.Error: {}".format(id, e))


def list_schema(page:int, size:int, deleted:bool=False):
    try:
        query = session.query(Schema)
        if not deleted:
            query = query.filter(Schema.deleted == False)
        return paginate(page, size, query)
    except Exception as e:
        logging.error("{}".format(e))


def paginate(page, size, query):
    try:
        page = page if page > 0 else 1
        size = size if size < 101 else 20
        count = query.count()
        pages = math.ceil(count / size)
        result = query.limit(size).offset(size * (page - 1)).all()
        return result, (page, size, pages)
    except Exception as e:
        logging.error("{}".format(e))


#获取字段
def get_field(schema_name:str, filed_name:str, deleted:bool=False):
    schema = get_schema_by_name(schema_name)
    if not schema:
        raise ValueError("{} is not TableName".format(schema_name))
    query = session.query(Field).filter((Field.name == filed_name) & (Field.schema_id == schema.id))
    if not deleted:
        query = query.filter(Field.deleted == False)
    return query.first()


#逻辑表是否使用
def table_use(schema_id, deleted:bool=False):
    query = session.query(Entity).filter(Entity.schema_id == schema_id)
    if not deleted:
        query.filter(Entity.deleted == False)
    return query.first() is not None


#直接添加字段
def _add_field(field:Field):
    session.add(field)
    try:
        session.commit()
        return field
    except Exception as e:
        session.rollback()
        logging.error("Failed to add a field {}. Error: {}".format(field.name, e))


def add_field(schema_name, name, meta):
    schema = get_schema_by_name(schema_name)
    if not schema:
        raise ValueError("{} is not a tablename".format(schema_name))
    meta_data = FieldMeta(meta)
    field = Field()
    field.schema_id = schema.id
    field.name = name.strip()
    field.meta = meta
    if meta_data.reference:
        ref = get_field(meta_data.reference.schema, meta_data.reference.field)
        if not ref:
            raise TypeError('Wrong Reference {}.{}'.format(meta_data.reference.schema,meta_data.reference.field))
        field.ref_id = ref.id
    if not table_use(schema.id):
        return _add_field(field)
    if meta_data.nullable:
        return _add_field(field)

    if meta_data.unique:
        raise TypeError('This field is required an unique')
    if not meta_data.default:

        raise TypeError('This field requires a default value')
    else:
        entityes = session.query(Entity).filter((Entity.schema_id == schema.id) & (Entity.deleted == False)).all()

        for entity in entityes:
            value = Value()
            value.entity_id = entity.id
            value.field = field
            value.value = meta_data.default
            session.add(value)
        return _add_field(field)










