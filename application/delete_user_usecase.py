from dataclasses import dataclass
from typing import Protocol

from domain.event import Event
from domain.user import User


class DeleteUserRepository(Protocol):
    def delete_user_by_id(self, id: int) -> None: ...


class IDispatcher(Protocol):
    async def send_events(self, *event: Event) -> None: ...


@dataclass
class Input:
    id: int


@dataclass
class Output:
    msg: str


class DeleteUserUsecase:
    def __init__(self, repo: DeleteUserRepository, dispatcher: IDispatcher) -> None:
        self._repo = repo
        self._dispatcher = dispatcher

    def execute(self, input: Input) -> Output:
        msg = self._repo.delete_user_by_id(id=input.id)
        return Output(msg=msg)
