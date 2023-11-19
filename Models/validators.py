from typing import Any
import re


class Validator:
    def __init__(self, required=False, min_len=0, max_len=0, dataType=str):
        self.required = required
        self.min_len = min_len
        self.max_len = max_len
        self.dataType = dataType

    def __call__(self, value):
        if self.required and value == None:
            return False
        elif self.dataType != type(value):
            return False
        elif (
            self.min_len != self.max_len
            and self.dataType == str
            and (self.min_len > len(value) or self.max_len < len(value))
        ):
            return False
        return True


class EmailValidator(Validator):
    def __init__(
        self,
        required=True,
        max_len=128,
    ):
        super().__init__(required, min_len=10, max_len=max_len)

    def __call__(self, value):
        return super().__call__(value) and self.validate_email(value)

    def validate_email(self, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, value):
            return True
        else:
            return False


class PasswordValidator(Validator):
    def __init__(
        self,
        required=True,
        max_len=128,
    ):
        super().__init__(required, min_len=7, max_len=max_len)

    def __call__(self, value):
        return super().__call__(value)
