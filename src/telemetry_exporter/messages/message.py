from datetime import datetime
from telemetry_exporter.protocols import AbstractMessage
from telemetry_exporter.exceptions import ExceptionMessageCreate


class Message(AbstractMessage):
    def __init__(self, created, _type, counters, labels=[]):
        self._data = counters
        self._created = created
        self._labels = labels
        self._type = _type

    @property
    def labels(self):
        return self._labels

    @property
    def type(self):
        return self._type

    @property
    def created(self):
        return datetime.fromtimestamp(self._created)

    @property
    def data(self):
        return self._data

    @classmethod
    def create(cls, created, _type, counters, labels):
        if not isinstance(labels, list):
            raise ExceptionMessageCreate('labels should be list')
        #
        #  NOTE: Add more validation here
        #
        return cls(created, _type, counters, labels)

    async def export(self, provider):
        _d = map(
            lambda f: (
                self.created,
                self.type.value,
                *f,
                self._labels,
            ), self.data)
        await provider.put(_d)

    @classmethod
    def decode(cls, serializer, payload):
        return cls(*serializer.decode(payload))

    def encode(self, serializer):
        return serializer.encode([
            self._created,
            self.type,
            self.data,
            self.labels,
        ])
