from telemetry_exporter.protocols import AbstractTransportConfig


class TransportConfigKafka(AbstractTransportConfig):
    def __init__(self):
        self._proto = None
        self._port = None
        self._host = None
        self._topic = None
        self._client_id = None
        self._group_id = None

        self._cafile = None
        self._certfile = None
        self._keyfile = None
        self._password = None

    @property
    def connection_uri(self):
        if not self.port or not self.host:
            raise Exception('provide correct hostname and port')
        return f'{self.host}:{self.port}'

    @property
    def host(self):
        if not self._host:
            raise Exception('host is empty')
        return self._host

    @host.setter
    def host(self, value):
        if not isinstance(value, str):
            raise AttributeError('host must be string')
        self._host = value

    @property
    def port(self):
        if not self._port:
            raise Exception('port is empty')
        return self._port

    @port.setter
    def port(self, value):
        if not isinstance(value, int):
            raise AttributeError('port must be integer')
        if value > 65535 or value <= 1024:
            raise AttributeError('wrong port value')

        self._port = value

    @property
    def proto(self):
        if not self._proto:
            raise Exception('proto is empty')
        return self._proto

    @proto.setter
    def proto(self, value):
        if value not in ['PLAINTEXT', 'SSL']:
            raise AttributeError('wrong proto')
        self._proto = value

    @property
    def topic(self):
        if not self._topic:
            raise Exception('topic is undefined')
        return self._topic

    @topic.setter
    def topic(self, value):
        if not isinstance(value, str):
            raise AttributeError('topic must be string')
        self._topic = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise AttributeError('client_id must be string')
        self._client_id = value

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        if not isinstance(value, str) and value is not None:
            raise AttributeError('group_id must be string')
        self._group_id = value

    @property
    def cafile(self):
        if self.proto == 'SSL' and not self._cafile:
            raise Exception('CA must defined with SSL proto')
        return self._cafile

    @cafile.setter
    def cafile(self, value):
        if not isinstance(value, str):
            raise AttributeError('CA must be string')
        self._cafile = value

    @property
    def certfile(self):
        if self.proto == 'SSL' and not self._certfile:
            raise Exception('cert must defined with SSL proto')
        return self._certfile

    @certfile.setter
    def certfile(self, value):
        if not isinstance(value, str):
            raise AttributeError('cert must be string')
        self._certfile = value

    @property
    def keyfile(self):
        if self.proto == 'SSL' and not self._keyfile:
            raise Exception('keyfile must defined with SSL proto')
        return self._keyfile

    @keyfile.setter
    def keyfile(self, value):
        if not isinstance(value, str):
            raise AttributeError('keyfile must be string')
        self._keyfile = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str) and value is not None:
            raise AttributeError('password must be string')
        self._password = value
