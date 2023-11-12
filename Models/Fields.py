from typing import Any
from wtforms import validators

from email_validator import validate_email, EmailNotValidError


class ValidationError(Exception):
    pass


class Validator:
    def __init__(self, value):
        self.value = value


class EmailValidator(Validator):
    def __call__(self) -> Any:
        if validate_email(self.value):
            return True
        return False


class Field:
    def __init__(self, value):
        self.value = value
        self.validators = []

    def validate(self):
        valid = False
        for validator in self.validators:
            valid = validator(self.value)
            print
            if not valid:
                break


class EmailField(Field):
    def __init__(self, value, min_len=32, max_len=128):
        self.validators = [
            validators.DataRequired("Email Required"),
            validators.Email(message="Invalid email address"),
            validators.Length(
                min=min_len,
                max=max_len,
                message=f"Email must be between {min_len} - {max_len}",
            ),
        ]
        super().__init__(value)


class PasswordField(Field):
    def __init__(self, value, min_len=32, max_len=128):
        self.validators = [
            validators.DataRequired(),
            validators.Length(min=min_len, max=max_len),
        ]
        super().__init__(value)


# Create an instance of EmailField
email_field = EmailField("humam")

# Call the validate method on the instance
email_field.validate()
