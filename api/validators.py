from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError


def custom_year_validator(value):
    if value >= datetime.now().year + settings.FUTURE_RELEASE:
        raise ValidationError(
            ('Year cant be longer than the current + 15 years'),
            params={'value': value},
        )
