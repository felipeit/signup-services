from typing import Any

from application.change_password_usecase import ChangePasswordUsecase
from application.delete_user_usecase import DeleteUserUsecase
from infra.fake_dispatcher import FakeDispatcher
from infra.rabbitq_dispatcher import RabbitMQDispatcher
from .models import User as UserRepository
from ninja import NinjaAPI, Schema


from application.signup_usecase import Input, SignupUsecase

api = NinjaAPI()


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


class UserApiInput(Schema):
    email: str
    password: str

@api.post("/signup")
def signup(request, input: UserApiInput) -> Any:
    usecase = SignupUsecase(repo=UserRepository, dispatcher=RabbitMQDispatcher())
    output = usecase.execute(input)
    return {"id": output.id}

class ChangePasswordInput(Schema):
    id: int
    password: str

@api.post("/change-password")
def change_password(request, input: ChangePasswordInput) -> Any:
    usecase = ChangePasswordUsecase(repo=UserRepository, dispatcher=RabbitMQDispatcher())
    output = usecase.execute(input)
    return {"id": output.id}

class DeleteUserInput(Schema):
    id: int

@api.delete("/delete-user")
def delete_user(request, input: DeleteUserInput) -> Any:
    usecase = DeleteUserUsecase(repo=UserRepository, dispatcher=RabbitMQDispatcher())
    output = usecase.execute(input)
    return {"response": output.msg }