import logging
import ssl
import asyncpg
from telemetry_exporter.protocols import AbstractDatabase, DATABASE_TYPE

logger = logging.getLogger(__name__)


class DatabasePgSQL(AbstractDatabase):
    def __init__(self, pool):
        self.__pool = pool

    @property
    def type(self):
        return DATABASE_TYPE.PGSQL

    async def put(self, payload):
        try:
            async with self.__pool.acquire() as con:
                #
                # NOTE: Actully telemetry not required transaction
                #       on usual cases. Transaction should abonded
                #
                async with con.transaction():
                    await con.executemany(
                        '''
                            INSERT INTO telemetry(
                                created,
                                metric,
                                key,
                                value,
                                labels
                            )
                            VALUES ($1, $2, $3, $4, $5)
                        ''',
                        payload
                    )
        except Exception:
            logger.error('error on insert telemetry', exc_info=True)

    @classmethod
    async def connect(cls, config):
        if config.cafile:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            ssl_context.load_verify_locations(config.cafile)
        else:
            ssl_context = None

        _pool = await asyncpg.create_pool(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
            ssl=ssl_context,
        )
        return cls(_pool)
