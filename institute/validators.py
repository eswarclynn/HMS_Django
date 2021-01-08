from datetime import date
from django.core.exceptions import ValidationError

def numeric_only(value: str):
    if not value.isnumeric():
        raise ValidationError("Phone number should be numeric.")

def date_no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('Cannot be in the future.')

def date_no_past(value):
    today = date.today()
    if value < today:
        raise ValidationError('Cannot be in the past.')
