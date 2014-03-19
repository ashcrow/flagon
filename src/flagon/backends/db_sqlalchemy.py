from sqlalchemy import Column, SmallInteger, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flagon import errors
from flagon.backends import Backend


Base = declarative_base()


class Feature(Base):
    __tablename__ = 'features'

    name = Column(String, primary_key=True)
    on = Column(SmallInteger)


class SQLAlchemyBackend(Backend):

    def __init__(self, connection_str):
        """
        connection_str information can be found at
            http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
        Example: sqlite:///test.db
        """
        self._engine = create_engine(connection_str, echo=False)
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine).__call__()

    def exists(self, name):
        return bool(self._session.query(Feature).filter_by(name=name).count())

    def is_on(self, name):
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        feature = self._session.query(Feature).filter_by(name=name).first()
        return bool(feature.on)

    def turn_on(self, name):
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._session.merge(Feature(name=name, on=1))
        self._session.commit()

    def turn_off(self, name):
        # TODO: Copy paste --- :-(
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._session.merge(Feature(name=name, on=0))
        self._session.commit()
