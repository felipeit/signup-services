class User:
    def __init__(self, email: str, password: str, id: int) -> None:
        self.email = email
        self.password = password
        self.id = id

    @classmethod
    def signup(cls, email:str, password:str) -> "User":
        return cls(email, password, id=None)