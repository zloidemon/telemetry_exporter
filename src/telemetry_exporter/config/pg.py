from telemetry_exporter.protocols import AbstractDatabaseConfig


class DatabaseConfigPgSQL(AbstractDatabaseConfig):
    def __init__(self):
        self._host = None
        self._port = None
        self._user = None
        self._password = None
        self._database = None
        self._cafile = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        if not isinstance(value, str):
            ValueError('host must be str')
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if not isinstance(value, int):
            ValueError('port must be int')
        self._port = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, str):
            ValueError('user must be str')
        self._user = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            ValueError('passsword must be str')
        self._password = value

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        if not isinstance(value, str):
            ValueError('database must be str')
        self._database = value

    @property
    def cafile(self):
        return self._cafile

    @cafile.setter
    def cafile(self, value):
        if not isinstance(value, str):
            ValueError('must be path')
        self._cafile = value
