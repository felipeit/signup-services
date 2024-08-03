from dataclasses import dataclass
from typing import Protocol

from domain.event import Event
from domain.user import User


class SignupRepository(Protocol):
    async def signup(self, user: User) -> None:
        pass


class IDispatcher(Protocol):
    async def send_events(self, *event: Event) -> None: ...


@dataclass
class Input:
    user: str
    password: str


@dataclass
class Output:
    id: int


class SignupUsecase:
    def __init__(self, repo: SignupRepository, dispatcher: IDispatcher) -> None:
        self._repo = repo
        self._dispatcher = dispatcher

    async def execute(self, input: Input) -> Output:
        user = User.signup(input.email, password=input.password)
        # await self._repo.signup(user)
        await self._dispatcher.send_events(*user.get_events())
        return Output(id=user.id)
