from abc import (
    ABCMeta,
    abstractmethod,
    abstractclassmethod,
    abstractproperty,
)
from enum import Enum, unique


@unique
class TRANSPORT_TYPE(Enum):
    KAFKA = 'kafka'
    RABBITMQ = 'rabbitmq'


class AbstractTransport(metaclass=ABCMeta):
    @abstractclassmethod
    async def connect(cls, serializer, config):
        pass

    @abstractproperty
    def type(self):
        pass

    @abstractmethod
    async def process(self, obj):
        pass


class AbstractTransportConfig(metaclass=ABCMeta):
    @abstractproperty
    def host(self):
        pass

    @abstractproperty
    def port(self):
        pass

    @abstractproperty
    def proto(self):
        pass
