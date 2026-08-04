from dataclasses import dataclass


@dataclass
class VM300012MDISParameter:
    ChannelPair12Type: int = 0
    ChannelPair34Type: int = 0
    channelactive: int = 0
    thrustdirection: int = 0