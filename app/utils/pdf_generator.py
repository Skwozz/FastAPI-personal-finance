from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_PATH = os.path.join("fonts", "DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))
def generate_pdf(transactions: list[dict]) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer,pagesize=letter)
    weight, height = letter
    c.setFont("DejaVuSans", 12)
    y = height - 50
    c.drawString(50, y, f"Финансовый отчёт от {datetime.now().strftime('%d.%m.%Y')}")
    y -= 30

    for tx in transactions:
        line = f"{tx['date']} |  {tx['description']} | {tx['amount']}руб"
        c.drawString(50, y, line)
        y -= 20

        if y < 50:
            c.showPage()
            c.setFont("DejaVuSans", 12)
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer