import logging
import asyncio
import time
import pathlib
import aiofiles

from telemetry_exporter.protocols import (
    AbstractMetric,
    LOADVG_VARIABLES,
    MESSAGE_TYPE,
)
from telemetry_exporter.messages import Message
from telemetry_exporter.exceptions import (
    ExceptionMessageCreate,
    ExceptionMessageParse,
)

logger = logging.getLogger(__name__)


class MetricLoadAvg(AbstractMetric):
    def __init__(self, queue, interval=10, trace=False, labels=[]):
        self.queue = queue
        self.interval = interval
        self.trace = trace
        self._proc_file = '/proc/loadavg'
        self._labels = labels

    def __parser(self, raw):
        try:
            data = raw.split()
            counters = (
                (LOADVG_VARIABLES.M1.value, float(data[0])),
                (LOADVG_VARIABLES.M5.value, float(data[1])),
                (LOADVG_VARIABLES.M15.value, float(data[2])),
            )
        except Exception:
            logger.error(
                f'can not parse {self._proc_file}',
                exc_info=True)
            raise ExceptionMessageParse(f'can not parse {self._proc_file}')
        return time.time(), MESSAGE_TYPE.LOADAVG, counters, self._labels

    async def start(self):
        while True:
            f = pathlib.Path(self._proc_file)

            if f.exists() is True:
                break

            logger.error(f'file {self._proc_file} not found')
            await asyncio.sleep(self.interval)

        logger.info(f'started {self.__class__.__name__}')

        async with aiofiles.open(self._proc_file, mode='r') as fh:
            while True:
                _message = None
                _data = await fh.read()
                await fh.seek(0)

                try:
                    parsed = self.__parser(_data)
                    _message = Message.create(*parsed)
                except ExceptionMessageCreate:
                    logger.error(
                        'not possible encode data',
                        exc_info=self.trace
                    )
                except ExceptionMessageParse:
                    logger.error(
                        'not possible parse data',
                        exc_info=self.trace
                    )
                except Exception:
                    logger.error(
                        'can not parse meminfo',
                        exc_info=self.trace)

                if _message:
                    try:
                        await self.queue.put(_message)
                    except asyncio.QueueFull:
                        logger.error('queue is full can not add new task')
                    except Exception:
                        logger.fatal(
                            'unknown exception',
                            exc_info=True)

                await asyncio.sleep(self.interval)
