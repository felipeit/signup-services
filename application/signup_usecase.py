
from dataclasses import dataclass
from domain.user import User
from typing import Protocol

class SignupRepository(Protocol):
    def signup(self, user:User) -> None:
        pass


@dataclass
class Input:
    user: str
    password: str

@dataclass
class Output:
    id: int

class SignupUsecase:
    def __init__(self, repo:SignupRepository) -> None:
        self._repo = repo

    def execute(self, input: Input) -> Output:  
        user = User.signup(input.email, password=input.password)
        self._repo.signup(user)
        return Output(id=user.id)