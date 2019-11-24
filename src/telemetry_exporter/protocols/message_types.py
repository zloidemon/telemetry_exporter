from enum import Enum, unique


@unique
class MESSAGE_TYPE(Enum):
    PING = 0
    ECHO = 1
    #
    # From 0 to 1999 reserved
    #
    MEMINFO = 2000
    LOADAVG = 2001
