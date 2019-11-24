import unittest
from telemetry_exporter.config import TransportConfigKafka


class TestTransportConfig(unittest.TestCase):

    def test_kafka_config_hostname(self):
        config = TransportConfigKafka()

        with self.assertRaises(AttributeError):
            config.host = 1234
        with self.assertRaises(AttributeError):
            config.host = None

        config.host = 'localhost'
        self.assertEqual('localhost', config.host)

    def test_kafka_config_port(self):
        config = TransportConfigKafka()

        with self.assertRaises(AttributeError):
            config.port = 'blah'
        with self.assertRaises(AttributeError):
            config.port = None
        with self.assertRaises(AttributeError):
            config.port = 0
        with self.assertRaises(AttributeError):
            config.port = -1
        with self.assertRaises(AttributeError):
            config.port = 65536
        with self.assertRaises(AttributeError):
            config.port = 1024

        config.port = 65535
        self.assertEqual(65535, config.port)
        config.port = 1025
        self.assertEqual(1025, config.port)

    def test_kafka_config_proto(self):
        config = TransportConfigKafka()

        with self.assertRaises(AttributeError):
            config.proto = 12312

        config.proto = 'PLAINTEXT'

        self.assertEqual('PLAINTEXT', config.proto)

        config.proto = 'SSL'

        self.assertEqual('SSL', config.proto)

    def test_kafka_config_topic(self):
        config = TransportConfigKafka()

        with self.assertRaises(AttributeError):
            config.topic = None
        with self.assertRaises(AttributeError):
            config.topic = 123
        config.topic = 'blah'

        self.assertEqual('blah', config.topic)

    def test_kafka_config_client_id(self):
        config = TransportConfigKafka()

        self.assertEqual(None, config.client_id)

        with self.assertRaises(AttributeError):
            config.client_id = 123
        config.client_id = 'blah'

        self.assertEqual('blah', config.client_id)
        config.client_id = None
        self.assertEqual(None, config.client_id)

    def test_kafka_config_group_id(self):
        config = TransportConfigKafka()

        self.assertEqual(None, config.group_id)

        with self.assertRaises(AttributeError):
            config.group_id = 123

        config.group_id = 'blah'

        self.assertEqual('blah', config.group_id)
        config.group_id = None
        self.assertEqual(None, config.group_id)
