from sqlalchemy import Column, Integer
from sqlalchemy.sql import text as sql
import importlib.resources
import sqlalchemy
import sqlalchemy.orm
import transaction
import ws.thyrida.interfaces
import zope.interface
import zope.sqlalchemy


@zope.interface.implementer(ws.thyrida.interfaces.IDatabase)
class Database(object):

    def __init__(self, dsn, testing=False):
        self.engine = sqlalchemy.create_engine(dsn, future=True)
        self.session_factory = sqlalchemy.orm.scoped_session(
            sqlalchemy.orm.sessionmaker(bind=self.engine, future=True))
        zope.sqlalchemy.register(self.session_factory, keep_session=testing)

    def initialize_database(self):  # mostly for tests
        from .mailbox import Mailbox
        try:
            with transaction.manager:
                Mailbox.query().all()
        except Exception:
            pass
        else:
            raise ValueError(
                'Database already exists, refusing to initialize again.')

        schema = importlib.resources.files(__package__).joinpath(
            'tests/schema.sql').read_text()
        for item in schema.split(';'):
            self.session.execute(sql(item))

    @property
    def session(self):
        return self.session_factory()

    def add(self, obj):
        return self.session.add(obj)

    def delete(self, obj):
        return self.session.delete(obj)

    def query(self, *args, **kw):
        return self.session.query(*args, **kw)


class ObjectBase(object):

    def __init__(self, **kw):
        super(ObjectBase, self).__init__()
        for key, value in kw.items():
            setattr(self, key, value)

    @staticmethod
    def db():
        return zope.component.getUtility(ws.thyrida.interfaces.IDatabase)

    @classmethod
    def query(cls):
        return cls.db().query(cls)

    @classmethod
    def find_by_id(cls, id):
        return cls.db().session.get(cls, id)

    @classmethod
    def find_by_sql(cls, text, **params):
        return cls.db().session.execute(
            cls.__table__.select().where(sql(text)),
            params=params).fetchall()


DeclarativeBase = sqlalchemy.orm.declarative_base(cls=ObjectBase)


class Object(DeclarativeBase):

    __abstract__ = True

    id = Column(Integer, primary_key=True)
