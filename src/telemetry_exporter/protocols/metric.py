from abc import ABCMeta, abstractmethod


class AbstractMetric(metaclass=ABCMeta):
    @abstractmethod
    async def start(self):
        pass
