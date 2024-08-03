import json
from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    identifier: str
    data: dict[str, str]
    created_at: datetime

    def asdict(self) -> dict[str, str]:
        repr = asdict(self)
        repr["data"]["created_at"] = self.created_at.isoformat()
        del repr["created_at"]
        return repr

    def __bytes__(self) -> bytes:
        return json.dumps(self.asdict()).encode()
