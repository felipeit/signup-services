from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    identifier:str
    data: dict[str, str]
    created_at: datetime