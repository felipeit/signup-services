from datetime import datetime
from typing import Any, Sequence

from .event import Event


class User:
    # 1 - Esse método serve para recuperar do banco/orm
    def __init__(self, email: str, password: str, id: int) -> None:
        self.email = email
        self.password = password
        self.id = id
        self._events: list[Event] = []
        self._created_at = datetime.now()

    # 2 - Esse método serve signup
    @classmethod
    def signup(cls, email: str, password: str) -> "User":
        user = cls(email, password, id=None)
        user_registered_event = Event(
            identifier="telegram.user-registered",
            data=dict(
                email=email,
                password=password,
            ),
            created_at=user._created_at,
        )
        user._events.append(user_registered_event)
        return user

    def change_password(self, password) -> Any:
        self.password = password

    def get_events(self) -> Sequence[Event]:
        return self._events
