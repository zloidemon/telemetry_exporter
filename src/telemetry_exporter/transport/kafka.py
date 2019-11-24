import logging
import asyncio

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

from telemetry_exporter.exceptions import ExceptionMessageEncode
from telemetry_exporter.protocols import (
    AbstractTransport,
    TRANSPORT_TYPE,
)
from telemetry_exporter.messages import Message


logger = logging.getLogger(__name__)


def get_context(config):
    if config.proto == 'SSL':
        context = create_ssl_context(
            cafile=config.cafile,
            certfile=config.certfile,
            keyfile=config.keyfile,
            password=config.password,
        )
    else:
        context = None
    return context


class TransportKafkaConsumer(AbstractTransport):
    def __init__(self, broker, serializer):
        self.__broker = broker
        self.__serializer = serializer

    async def process(self, provider):
        try:
            async for msg in self.__broker:
                logger.debug(
                    f't: {msg.timestamp} '
                    f't: {msg.topic} p: {msg.partition}, '
                    f'o: {msg.offset} k: {msg.key} v: {msg.value}'
                )
                try:
                    _message = Message.decode(self.__serializer, msg.value)
                except ExceptionMessageEncode:
                    logger.error('can not unpack message', exc_info=True)
                    continue
                logger.info(
                    f'{self.__broker._client._client_id}[{msg.partition}] '
                    f'm: {_message.type.name}')
                await _message.export(provider)
        except Exception:
            logger.error('got error while reading stream', exc_info=True)

    @property
    def type(self):
        return TRANSPORT_TYPE.KAFKA

    @classmethod
    async def connect(cls, serializer, config):
        _broker = AIOKafkaConsumer(
            config.topic,
            bootstrap_servers=config.connection_uri,
            loop=asyncio.get_running_loop(),
            client_id=config.client_id,
            group_id=config.group_id,
            security_protocol=config.proto,
            ssl_context=get_context(config),
        )
        await _broker.start()

        return cls(_broker, serializer)


class TransportKafkaProducer(AbstractTransport):
    def __init__(self, broker, serializer, config):
        self.__broker = broker
        self.__topic = config.topic
        self.__serializer = serializer

    async def process(self, message):
        try:
            await self.__broker.send_and_wait(
                self.__topic, message.encode(self.__serializer)
            )
        except Exception:
            logger.error('got error while send data', exc_info=True)

    @property
    def type(self):
        return TRANSPORT_TYPE.KAFKA

    @classmethod
    async def connect(cls, serializer, config):
        _broker = AIOKafkaProducer(
            bootstrap_servers=config.connection_uri,
            loop=asyncio.get_running_loop(),
            security_protocol=config.proto,
            ssl_context=get_context(config),
        )
        await _broker.start()

        return cls(_broker, serializer, config)
