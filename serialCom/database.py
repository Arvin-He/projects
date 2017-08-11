# -*- encoding:utf-8 -*-
import os
import json
import contextlib
import sqlalchemy
from sqlalchemy import create_engine, MetaData, String, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.sql import select, operators, text
from sqlalchemy.ext.mutable import MutableDict
from logger import logger

data_dir = os.path.abspath('userdata')
if not os.path.exists(data_dir):
    os.mkdir(data_dir)


class DataBase(object):

    def __init__(self, name, echo=False):
        self.name = name
        self.path = os.path.abspath(os.path.join(data_dir, self.name))
        url = "sqlite:///" + self.path
        # _logger.debug("engine: {}".format(url))
        self.engine = create_engine(url, echo=echo)
        self.BaseModel = declarative_base()
        self.Session = orm.sessionmaker(bind=self.engine)
        self.loadError = False

    def name(self):
        return self.name[:-3]

    def path(self):
        return self.path

    def _recovery(self):
        """恢复数据"""
        pass

    def _createAll(self):
        try:
            self.BaseModel.metadata.create_all(self.engine)
        except:
            self.loadError = True
            os.remove(self.path)
            self.BaseModel.metadata.create_all(self.engine)
            self._recovery()

    @contextlib.contextmanager
    def getSession(self):
        """创建一个会话, 以访问数据库"""
        self._createAll()
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        # logger.info("session open")
        try:
            yield session
            session.commit()
            # logger.info("session commit")
        except:
            session.rollback()
            # logger.info("session rollback")
            raise
        finally:
            session.close()
            # logger.info("session close")

    @contextlib.contextmanager
    def getQuery(self, *entities, **kwargs):
        with self.getSession() as session:
            query = session.query(*entities, **kwargs)
            yield query

    def __doJob(self, method, session, instances):
        _func = getattr(session, method)
        if isinstance(instances, list):
            for instance in instances:
                _func(instance)
        else:
            _func(instances)

    def __add(self, session, instances):
        if isinstance(instances, list):
            session.add_all(instances)
        else:
            session.add(instances)

    def add(self, instances, session=None):
        if session:
            self.__add(session, instances)
        else:
            with self.getSession() as session:
                self.__add(session, instances)

    def delete(self, instances, session=None):
        if session:
            self.__doJob('delete', session, instances)
        else:
            with self.getSession() as session:
                self.__doJob('delete', session, instances)

    def merge(self, instances, session=None):
        if session:
            self.__doJob('merge', session, instances)
        else:
            with self.getSession() as session:
                self.__doJob('merge', session, instances)

    def expunge(self, instances=None, session=None):
        if session:
            self.__doJob('expunge', session, instances)
        else:
            with self.getSession() as session:
                self.__doJob('expunge', session, instances)

    def execute(self, clause, params=None):
        with self.getSession() as session:
            session.execute(clause, params)

    def flush(self, objects=None):
        with self.getSession() as session:
            session.flush(objects)

    def createTable(self, cls):
        table = cls.__table__
        if table.exists(self.engine):
            return
        table.create(self.engine)

    def dropTable(self, cls):
        table = cls.__table__
        if table.exists(self.engine):
            table.drop(self.engine)

    def clearTable(self, cls):
        table = cls.__table__
        with self.engine.begin() as connection:
            connection.execute(table.delete())

    def listTables(self):
        meta = MetaData()
        meta.reflect(self.engine)
        return meta.tables

    def getMappedClasses(self):
        models = []

        def _querySubClasses(model):
            nonlocal models
            if model.__subclasses__():
                for sub in model.__subclasses__():
                    _querySubClasses(sub)
            else:
                models.append(model)

        _querySubClasses(self.BaseModel)
        return models

    def load(self, data, wanted=None):
        tables = self.metadata.tables
        if not wanted:
            wanted = {"table": set(tables.keys()), "specific": {}}

        with self.engine.begin() as connection:     # runs a transaction
            for k, v in data.items():
                if k not in wanted["table"]:
                    continue
                model = tables.get(k)
                if model is None:
                    continue
                _tags = wanted["specific"].get(k)

                if _tags:
                    connection.execute(
                        model.delete().where(model.c.tag.in_(_tags)))
                    filtered = filter(lambda d: d if d.get(
                        'tag') in _tags else None, v)
                    rec = list(filtered)
                    # connection.execute(model.insert(), list(filtered))
                else:
                    connection.execute(model.delete())
                    rec = v
                if rec:
                    connection.execute(model.insert(), rec)

    def dump(self, wanted=None):
        data = {}
        header = {"table": set(), "specific": dict()}
        tables = self.metadata.tables
        if not wanted:
            wanted = {"table": set(tables.keys()), "specific": {}}

        with self.engine.begin() as connection:     # runs a transaction
            for t in wanted["table"]:
                if t in wanted["specific"].keys():
                    name = t
                    tags = wanted["specific"][t]
                else:
                    name, tags = t, None

                model = tables.get(name)
                if model is None:
                    continue
                header["table"].add(name)
                if not tags:
                    res = connection.execute(select([model]))
                else:
                    header["specific"][name] = tags
                    res = connection.execute(
                        select([model]).where(model.c.tag.in_(tags)))

                data[name] = [dict(r) for r in res]
        return data, header

    @property
    def metadata(self):
        return self.BaseModel.metadata


# class JSONEncodedDict(TypeDecorator):
#     impl = VARCHAR

#     def coerce_compared_value(self, op, value):
#         if op in (operators.like_op, operators.notlike_op):
#             return String()
#         else:
#             return self

#     def process_bind_param(self, value, dialect):
#         if value is not None:
#             value = json.dumps(value)
#         return value

#     def process_result_value(self, value, dialect):
#         if value is not None:
#             value = json.loads(value)
#         return value

# sqlalchemy.JsonType = MutableDict.as_mutable(JSONEncodedDict)

db = DataBase("user_data.db")
