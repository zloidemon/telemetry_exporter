import logging
import asyncio
from enum import Enum, unique
import re
import time
import pathlib
import aiofiles
from telemetry_exporter.protocols import (
    AbstractMetric,
    MEMINFO_COUNTER,
    MESSAGE_TYPE,
)
from telemetry_exporter.messages import Message
from telemetry_exporter.exceptions import ExceptionMessageCreate


logger = logging.getLogger(__name__)


@unique
class MEMINFO_SCALE(Enum):
    kB = 1024


class MetricMeminfo(AbstractMetric):
    def __init__(self, queue, interval=10, trace=False, labels=[]):
        self.queue = queue
        self.interval = interval
        self.trace = trace
        self._proc_file = '/proc/meminfo'
        self._labels = labels

    def __parser(self, data):
        counters = tuple()

        for row in data.split('\n'):
            try:
                k, payload = row.split(':')
                key = MEMINFO_COUNTER[k]
            except ValueError:
                if row and row != '':
                    logger.error(
                        f'can not parse row {row}',
                        exc_info=self.trace)
                continue

            result_m = re.match(r'(\d+)(.*)?', payload.strip())

            if result_m:
                data, scale = result_m.group(1, 2)
                value = int(data)
                scale = scale.strip()

                if value > 0:
                    try:
                        value = value * MEMINFO_SCALE[scale].value
                    except KeyError:
                        logging.error(f'can not scaling fix me: {scale}')
                        continue
                    except Exception:
                        logger.error('unknown exception', exc_info=True)
                        continue
            else:
                logger.warning(f'not matched {key.name}')
                continue
            counters += (key.value, value),  # Yeah, tuple of tuples
        return time.time(), MESSAGE_TYPE.MEMINFO, counters, self._labels

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
