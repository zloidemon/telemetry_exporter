from abc import (
    ABCMeta,
    abstractmethod,
    abstractclassmethod,
    abstractproperty,
)
from enum import Enum, unique


@unique
class DATABASE_TYPE(Enum):
    PGSQL = 'pgsql'
    MYSQL = 'mysql'


class AbstractDatabase(metaclass=ABCMeta):
    @abstractmethod
    async def put(self, payload):
        pass

    @abstractproperty
    def type(self):
        pass

    @abstractclassmethod
    async def connect(cls, config):
        pass

    def __repr__(self):
        return f'<Database({self.type.name})>'


class AbstractDatabaseConfig(metaclass=ABCMeta):
    @abstractproperty
    def host(self):
        pass

    @abstractproperty
    def port(self):
        pass

    @abstractproperty
    def user(self):
        pass

    @abstractproperty
    def password(self):
        pass

    @abstractproperty
    def database(self):
        pass

    def __repr__(self):
        return f'<DatabaseConfig(' \
            f'{self.user}@{self.host}:{self.port}/{self.database})>'
