from django.core.exceptions import ValidationError


class IncludeValidator:

    def __init__(self, upper=True, lower=True, digit=True):
        self.upper = upper
        self.lower = lower
        self.digit = digit

    def validate(self, password, user=None):
        is_valid = any(char.isdigit() for char in password) and\
                   any(char.isupper() for char in password) and\
                   any(char.islower() for char in password)
        if not is_valid:
            raise ValidationError(
                self.get_help_text(),
                code='password too simple'
            )

    def get_help_text(self):
        msg = "This password is too simple, it must include at least:"
        if self.upper:
            msg += " one uppercase character,"
        if self.lower:
            msg += " one lowercase character,"
        if self.digit:
            msg += " one numeric character,"
        msg = msg[:-1]+'.'
        return msg
