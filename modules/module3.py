from dataclasses import dataclass
from typing import Any


@dataclass
class Channels:
    Channel_active: Any = None
    Channel_latching: Any = None
    channel_NE_NDE: Any = None