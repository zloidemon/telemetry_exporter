import json
from telemetry_exporter.protocols import AbstractSerializer, MESSAGE_TYPE
from telemetry_exporter.exceptions import ExceptionMessageEncode


class SerializerJson(AbstractSerializer):
    @staticmethod
    def decode(payload):
        try:
            data = json.loads(payload.decode())
            data[1] = MESSAGE_TYPE(data[1])
            SerializerJson.validate(data)
        except json.decoder.JSONDecodeError:
            raise ExceptionMessageEncode('invalid data')
        return data

    @staticmethod
    def encode(payload):
        SerializerJson.validate(payload)

        binary = json.dumps([
            payload[0],
            payload[1].value,
            payload[2],
            payload[3],
        ]).encode()
        return binary
