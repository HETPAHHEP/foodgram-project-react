import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class HexColorValidator:
    """Валидатор hex-кода цвета"""
    regex = r'^#([A-Fa-f0-9]{6})$'
    message = _('Цвет не соответствует hex кодировке')
    error_code = 'errors'

    def __init__(self, pattern=regex, detail=message, code=error_code):
        self.pattern = pattern
        self.detail = detail
        self.code = code

    def __call__(self, value):
        if not re.match(self.pattern, self.detail):
            raise ValidationError(detail=self.detail, code=self.code)
