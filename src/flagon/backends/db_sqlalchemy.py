from sqlalchemy import (
    Column, Integer, SmallInteger, String, ForeignKey, create_engine)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flagon import errors
from flagon.backends import Backend


Base = declarative_base()


class Feature(Base):
    __tablename__ = 'features'

    name = Column(String, primary_key=True)
    active = Column(SmallInteger)
    strategy = Column(String)
    params = relationship('Param', backref='feature')


class Param(Base):
    __tablename__ = 'params'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    feature_id = Column(Integer, ForeignKey('features.name'))


class SQLAlchemyBackend(Backend):

    def __init__(self, connection_str):
        """
        :param connection_str: information can be found at
            http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
            Example: sqlite:///test.db
        :type connection_str: str
        :rtpe: SQLAlchemyBackend
        """
        self._engine = create_engine(connection_str, echo=False)
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine).__call__()

    def exists(self, name):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        return bool(self._session.query(Feature).filter_by(name=name).count())

    def is_active(self, name):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        feature = self._session.query(Feature).filter_by(name=name).first()
        return bool(feature.active)

    def _turn(self, name, value):
        """
        Turns a feature on or off

        :param name: name of the feature.
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        data = self._read_file()
        data[name]['active'] = bool(value)
        self._write_file(data)

    def _turn(self, name, value):
        """
        Turns a feature on.

        :param name: name of the feature.
        :param value: 0 or 1
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._session.merge(Feature(name=name, active=value))
        self._session.commit()

    turn_on = lambda s, name: _turn(s, name, 1)
    turn_off = lambda s, name: _turn(s, name, 2)
