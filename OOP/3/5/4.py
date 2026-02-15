class UserMail:
    logins = set()
    def __init__(self, login, email):
        self.login = login
        self.email = email

    def login(self):
        return self.__login

    def login(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{value} не является строкой")

        if value in UserMail.logins:
             if not hasattr(self, "_UserMail__login") or self.__login != value:
                raise ValueError(f"Логин {value} уже имеется в системе")


        if hasattr(self, "_UserMail__login"):
            UserMail.logins.discard(self.__login)

        self.__login = value
        UserMail.logins.add(value)