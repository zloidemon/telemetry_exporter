from abc import (
    ABCMeta,
    abstractproperty,
    abstractclassmethod,
    abstractmethod,
)


class AbstractMessage(metaclass=ABCMeta):
    @abstractclassmethod
    def create(cls, created, _type, counters, labels):
        pass

    @abstractclassmethod
    def decode(cls, serializer, payload):
        pass

    @abstractmethod
    def encode(self, serializer):
        pass

    @abstractproperty
    def labels(self):
        pass

    @abstractproperty
    def type(self):
        pass

    @abstractproperty
    def created(self):
        pass

    @abstractproperty
    def data(self):
        pass

    @abstractmethod
    async def export(self, provider):
        pass

    def __repr__(self):
        return f'<Message(' \
            f'type={self.type.name}, ' \
            f'created="{self.created}", ' \
            f'counters={len(self.data)})>'
