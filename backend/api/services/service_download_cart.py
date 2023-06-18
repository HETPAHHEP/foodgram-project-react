import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def download_cart_pdf(shopping_list):
    title = 'Список продуктов'

    pdfmetrics.registerFont(
        TTFont(
            'Vasek',
            'data/fonts/Vasek.ttf'
        )
    )
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer)

    pdf_file.setFont('Vasek', 50)
    pdf_file.drawString(200, 790, title)
    pdf_file.setFont('Vasek', 30)

    height = 740
    width = 75

    for numb, item in enumerate(shopping_list, 1):
        pdf_file.drawString(width, height, (
            f'{numb}. {str(item["ingredient__name"]).capitalize()} '
            f'- {item["amount"]} '
            f'{item["ingredient__measurement_unit"]}'))
        height -= 40

    pdf_file.showPage()
    pdf_file.save()
    buffer.seek(0)

    return buffer
