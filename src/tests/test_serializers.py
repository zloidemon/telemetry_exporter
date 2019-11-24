import unittest
from telemetry_exporter.protocols import MESSAGE_TYPE, MEMINFO_COUNTER
from telemetry_exporter.exceptions import ExceptionMessageEncode
from telemetry_exporter.serializers import (
    SerializerJson,
    SerializerMessagePack,
)
import socket
import msgpack
import random
import time


class TestSerializers(unittest.TestCase):

    def setUp(self):
        self.serializers = [
            SerializerMessagePack,
            SerializerJson,
        ]

    def test_encode(self):
        for serializer in self.serializers:
            with self.assertRaises(Exception):
                serializer.encode({'aaaa': 123})

            with self.assertRaises(TypeError):
                serializer.encode([1, 1, 1, 1])

            with self.assertRaises(ValueError):
                serializer.encode([1, MEMINFO_COUNTER(1), 1, 1])

            with self.assertRaises(ValueError):
                serializer.encode([1, MESSAGE_TYPE.MEMINFO, 1, 1])

            with self.assertRaises(ValueError):
                serializer.encode([1, MESSAGE_TYPE.MEMINFO, set({1}), 1])

            with self.assertRaises(TypeError):
                serializer.encode([1, MESSAGE_TYPE.MEMINFO, [1], 1])

            with self.assertRaises(ValueError):
                serializer.encode([1, MESSAGE_TYPE.MEMINFO, {}, 1])

            with self.assertRaises(ValueError):
                serializer.encode([1, MESSAGE_TYPE.MEMINFO, [(1, 1)], 1])

            with self.assertRaises(ValueError):
                serializer.encode([
                    1, MESSAGE_TYPE.MEMINFO, [(1, 1)], set({1})
                ])

            with self.assertRaises(ValueError):
                serializer.encode([1, MESSAGE_TYPE.MEMINFO, [(1, 1)], [1]])

    def test_json_decode(self):
        timestamp = time.time()

        self.assertEqual(
            [timestamp, MESSAGE_TYPE.LOADAVG, [[3, 1]], []],
            SerializerJson.decode((f'[{timestamp},2001,[[3,1]],[]]').encode())
        )

        with self.assertRaises(ExceptionMessageEncode):
            SerializerJson.decode((f'[{timestamp},2001,[[3,1],[]]').encode())

        with self.assertRaises(ValueError):
            SerializerJson.decode((f'[{timestamp},2001,[[3]],[]]').encode())

        with self.assertRaises(ValueError):
            SerializerJson.decode(
                (f'[{timestamp},2001,[[3, "x"]],[]]').encode())

        with self.assertRaises(ValueError):
            SerializerJson.decode(
                (f'[{timestamp},2001,[["3", "x"]],[]]').encode())

        with self.assertRaises(ValueError):
            SerializerJson.decode((f'[{timestamp},"A",[[1,1]],[]]').encode())

        with self.assertRaises(ValueError):
            SerializerJson.decode((f'[{timestamp},[],[[1,1]],[]]').encode())

    def test_mpack_decode(self):
        with self.assertRaises(TypeError):
            SerializerMessagePack.decode('asdfsa')

        with self.assertRaises(TypeError):
            SerializerMessagePack.decode(1234)

        with self.assertRaises(ExceptionMessageEncode):
            SerializerMessagePack.decode(b'123')

        with self.assertRaises(ValueError):
            SerializerMessagePack.decode(msgpack.packb([1, 2, 3, 4]))

        with self.assertRaises(IndexError):
            SerializerMessagePack.decode(msgpack.packb(['abc']))

        with self.assertRaises(ValueError):
            SerializerMessagePack.decode(msgpack.packb([1, 'abc', 2, 3]))

        with self.assertRaises(ValueError):
            SerializerMessagePack.decode(msgpack.packb([1, 2001, 2, 3]))

        with self.assertRaises(TypeError):
            SerializerMessagePack.decode(msgpack.packb([1, 2001, [2], 3]))

        with self.assertRaises(ValueError):
            SerializerMessagePack.decode(msgpack.packb([1, 2001, [(1, 2)], 3]))

        with self.assertRaises(ValueError):
            SerializerMessagePack.decode(
                msgpack.packb([1, 2001, [(1, 2)], [3]])
            )

    def test_pack_unpack(self):
        for serializer in self.serializers:
            timestamp = time.time()

            frame = [
                timestamp, MESSAGE_TYPE.MEMINFO,
                [
                    [c.value, random.randint(0, 100000000000)]
                    for c in MEMINFO_COUNTER
                ],
                [socket.gethostname()]
            ]

            packed = serializer.encode(frame)

            self.assertEqual(frame, serializer.decode(packed))
