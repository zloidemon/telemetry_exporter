from telemetry_exporter.protocols import (
    AbstractTransport,
    TRANSPORT_TYPE,
)


class TransportRabbitMQConsumer(AbstractTransport):
    def __init__(self, broker):
        raise NotImplementedError('Implement me')

    async def process(self, provider):
        raise NotImplementedError('Implement me')

    @property
    def type(self):
        return TRANSPORT_TYPE.RABBITMQ

    @classmethod
    async def connect(cls, serializer, host=None, topic=None):
        raise NotImplementedError('Implement me')


class TransportRabbitMQProducer(AbstractTransport):
    def __init__(self, broker, topic):
        raise NotImplementedError('Implement me')

    async def process(self, message):
        raise NotImplementedError('Implement me')

    @property
    def type(self):
        return TRANSPORT_TYPE.RABBITMQ

    @classmethod
    async def connect(cls, serializer, host=None, topic=None):
        raise NotImplementedError('Implement me')
