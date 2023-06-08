from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class HexColorValidator(RegexValidator):
    """Валидатор hex-кода цвета"""
    regex = r'^#([A-Fa-f0-9]{6})$'
    message = _('Цвет не соответствует hex кодировке')
    code = 'invalid_hex_color'
