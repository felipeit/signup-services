from typing import Any
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
    usecase = SignupUsecase(repo=UserRepository)
    output = usecase.execute(input)
    return {"id": output.id}
