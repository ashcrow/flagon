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
        return bool(feature.on)

    def turn_on(self, name):
        """
        Turns a feature on.

        :param name: name of the feature.
        :raises: UnknownFeatureError
        """
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._session.merge(Feature(name=name, on=1))
        self._session.commit()

    def turn_off(self, name):
        """
        Turns a feature off.

        :param name: name of the feature.
        :raises: UnknownFeatureError
        """
        # TODO: Copy paste --- :-(
        if not self.exists(name):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        self._session.merge(Feature(name=name, on=0))
        self._session.commit()
