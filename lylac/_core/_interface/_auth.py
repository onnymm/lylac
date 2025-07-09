from typing import Literal

class Auth_Interface():

    def identify_user(
        self,
        token: str,
    ) -> int:
        ...

    def hash_password(
        self,
        password: str,
    ) -> str:
        ...

    def login(
        self,
        login: str,
        password: str,
    ) -> str | Literal[False]:
        ...
