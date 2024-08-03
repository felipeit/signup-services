from dataclasses import dataclass
from typing import Protocol

from domain.event import Event
from domain.user import User


class ChangePasswordRepository(Protocol):
    def get_user_by_id(self, id: int) -> User: ...
    def change_password(self, user: User) -> None: ...


class IDispatcher(Protocol):
    async def send_events(self, *event: Event) -> None: ...


@dataclass
class Input:
    id: int
    password: str


@dataclass
class Output:
    id: int


class ChangePasswordUsecase:
    def __init__(self, repo: ChangePasswordRepository, dispatcher: IDispatcher) -> None:
        self._repo = repo
        self._dispatcher = dispatcher

    def execute(self, input: Input) -> Output:
        user = self._repo.get_user_by_id(id=input.id)
        user.change_password(password=input.password)
        self._repo.change_password(user)
        return Output(id=user.id)
