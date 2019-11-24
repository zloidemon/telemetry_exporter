from telemetry_exporter.protocols import AbstractDatabase, DATABASE_TYPE


class DatabaseMySQL(AbstractDatabase):
    def __init__(self, pool):
        self.__pool = pool

    @property
    def type(self):
        return DATABASE_TYPE.MYSQL

    async def put(self, payload):
        raise NotImplementedError('Implement me')

    @classmethod
    async def connect(cls, config):
        raise NotImplementedError('Implement me')
