from abc import ABCMeta, abstractstaticmethod
from .message_types import MESSAGE_TYPE


class AbstractSerializer(metaclass=ABCMeta):
    @staticmethod
    def check_message_type(value):
        if value not in MESSAGE_TYPE:
            raise ValueError('non MESSAGE_TYPE')

    @staticmethod
    def check_message_data(value):
        if not isinstance(value, list) and \
                not isinstance(value, tuple):
            raise ValueError('data should be list or tuple')

        if len(value) < 1:
            raise AttributeError('dataset is empty')

        for counter, val in value:
            if not isinstance(counter, int):
                raise ValueError('counter must be integer')
            if not isinstance(val, int) and \
                    not isinstance(val, float):
                raise ValueError('value must be integer')

    @staticmethod
    def check_message_labels(value):
        if not isinstance(value, list) and \
                not isinstance(value, tuple):
            raise ValueError('data should be list or tuple')

        for label in value:
            if not isinstance(label, str):
                raise ValueError('label must be string')

    @staticmethod
    def validate(payload):
        if len(payload) != 4:
            raise Exception('not enough data in message')

        AbstractSerializer.check_message_type(payload[1])
        AbstractSerializer.check_message_data(payload[2])
        AbstractSerializer.check_message_labels(payload[3])

    @abstractstaticmethod
    def decode(payload):
        pass

    @abstractstaticmethod
    def encode(payload):
        pass
