
from dataclasses import dataclass
from domain.events import Event
from domain.user import User
from typing import Protocol

class SignupRepository(Protocol):
    def signup(self, user:User) -> None:
        pass

class IDispatcher(Protocol):
    def send_events(self, *event: Event) -> None: ...



@dataclass
class Input:
    user: str
    password: str

@dataclass
class Output:
    id: int

class SignupUsecase:
    def __init__(self, repo:SignupRepository, dispatcher: IDispatcher) -> None:
        self._repo = repo
        self._dispatcher = dispatcher

    def execute(self, input: Input) -> Output:  
        user = User.signup(input.email, password=input.password)
        self._repo.signup(user)
        self._dispatcher.send_events(*user.get_events())
        return Output(id=user.id)