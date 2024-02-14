import re
from datetime import datetime


class Validator:
    emailRegExp = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b")
    phoneNumberRegex = re.compile(r"^\+?[1-9][0-9]{7,14}$")

    @classmethod
    def validate_email(cls, value: str) -> str | None:
        if not value:
            return "Email cannot be empty"
        elif not cls.emailRegExp.match(value):
            return "Email is not valid"

    @classmethod
    def validate_phone_number(cls, value: str) -> str | None:
        if not value:
            return "Phone Number cannot be empty"
        elif not cls.phoneNumberRegex.match(value):
            return "Phone Number is not valid"

    @classmethod
    def validate_email_or_phone_number(cls, value: str) -> str | None:
        if not value:
            return "Email or Phone Number cannot be empty"
        else:
            return (
                ("@" in value)
                and cls.validate_email(value)
                or cls.validate_phone_number(value)
            )

    @classmethod
    def validate(cls, value: str, identifier: str):
        if not value:
            return f"{identifier} cannot be empty"

    @classmethod
    def validate_password(cls, value: str) -> str | None:
        if not value:
            return "Password cannot be empty"
        if len(value) < 6:
            return "Password must be at least 6 characters"

    @classmethod
    def validate_compare(
        cls,
        value1: str,
        value2: str,
        message: str,
    ) -> str | None:
        if value1 != value2:
            return message

    @classmethod
    def validate_among(
        cls,
        value: str,
        values: list[str],
        identifier: str,
    ) -> str | None:
        if value not in values:
            return f"{identifier} not among " + "".join(
                [f"`{value}`" for value in values]
            )

    @classmethod
    def validate_pin(cls, value: str) -> str | None:
        if len(value) != 4:
            return "Please enter 4 digits"

        if not value:
            return "Please enter code"

    @classmethod
    def validate_date(cls, date: str):
        try:
            day, month, year = date.split("-")
            day = int(day)
            month = int(month)
            year = int(year)
            date = datetime(year, month, day)

        except Exception as e:
            return (
                "Invalid date format, correct format is `dd-mm-yyyy` e.g `26-07-1999`"
            )
