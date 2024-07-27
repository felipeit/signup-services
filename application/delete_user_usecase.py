from dataclasses import dataclass
from domain.events import Event
from domain.user import User
from typing import Protocol

class DeleteUserRepository(Protocol): 
    def delete_user_by_id(self, id:int) -> None:...

class IDispatcher(Protocol):
    def send_events(self, *event: Event) -> None: ...

@dataclass
class Input:
    id: int

@dataclass
class Output:
    msg: str

class DeleteUserUsecase:
    def __init__(self, repo:DeleteUserRepository, dispatcher: IDispatcher) -> None:
        self._repo = repo
        self._dispatcher = dispatcher
        
    def execute(self, input: Input) -> Output:  
        msg = self._repo.delete_user_by_id(id=input.id)
        return Output(msg=msg)