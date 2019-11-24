from telemetry_exporter.protocols import AbstractSerializer, MESSAGE_TYPE
from telemetry_exporter.exceptions import ExceptionMessageEncode
import msgpack


class SerializerMessagePack(AbstractSerializer):
    @staticmethod
    def decode(payload):
        try:
            data = msgpack.unpackb(payload, raw=False)
            data[1] = MESSAGE_TYPE(data[1])
            SerializerMessagePack.validate(data)
        except msgpack.exceptions.ExtraData:
            raise ExceptionMessageEncode('invalid data')
        return data

    @staticmethod
    def encode(payload):
        SerializerMessagePack.validate(payload)

        binary = msgpack.packb([
            payload[0],
            payload[1].value,
            payload[2],
            payload[3],
        ])

        return binary
