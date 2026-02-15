class UserMail:
    def __init__(self, login, email):
        self.login = login
        self.email = email

    def get_email(self):
        return self.__email

    def set_email(self, new_email):
        if not isinstance(new_email, str):
            raise ValueError(f"ErrorMail:{new_email}")

        if new_email.count("@") == 1 and "." in new_email.split("@")[1]:
            self.__email = new_email
        else:
            raise ValueError(f"ErrorMail:{new_email}")

    email = property(fget=get_email, fset=set_email)
