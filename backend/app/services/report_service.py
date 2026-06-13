import os
from datetime import date
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

APP_NAME = "Bebeğim"
APP_TAGLINE = "Gebelik Takip"
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"


def _register_unicode_font() -> str:
    candidates = [
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", "arial.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont("ReportFont", path))
            return "ReportFont"
    return "Helvetica"


def _fmt(value, suffix: str = "") -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, float):
        text = f"{value:g}"
    else:
        text = str(value)
    return f"{text}{suffix}" if suffix else text


def _fmt_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        parts = value.split("-")
        if len(parts) == 3:
            return f"{parts[2]}.{parts[1]}.{parts[0]}"
    except Exception:
        pass
    return value


def _make_page_callbacks(font_name: str):
    def _draw_branding(canvas, _doc):
        page_width, page_height = A4
        x_right = page_width - 1.5 * cm
        y_top = page_height - 1.5 * cm
        logo_size = 1.1 * cm
        text_x = x_right

        if LOGO_PATH.is_file():
            canvas.drawImage(
                str(LOGO_PATH),
                x_right - logo_size,
                y_top - logo_size,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
                mask="auto",
            )
            text_x = x_right - logo_size - 0.3 * cm

        canvas.setFont(font_name, 11)
        canvas.setFillColor(colors.HexColor("#4a044e"))
        canvas.drawRightString(text_x, y_top - 0.35 * cm, APP_NAME)
        canvas.setFont(font_name, 8)
        canvas.setFillColor(colors.HexColor("#6b7280"))
        canvas.drawRightString(text_x, y_top - 0.7 * cm, APP_TAGLINE)

    return _draw_branding, _draw_branding


def generate_report_pdf(
    user_logs: list[dict],
    start_date: date,
    end_date: date,
    user_name: str | None = None,
) -> bytes:
    font_name = _register_unicode_font()
    buffer = BytesIO()
    on_first_page, on_later_pages = _make_page_callbacks(font_name)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2.8 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleTR",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=18,
        spaceAfter=8,
    )
    subtitle_style = ParagraphStyle(
        "SubtitleTR",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=16,
    )

    range_text = (
        f"{start_date.strftime('%d.%m.%Y')} – {end_date.strftime('%d.%m.%Y')}"
    )
    story = [
        Paragraph("Sağlık Takibi Raporu", title_style),
        Paragraph(
            f"Tarih aralığı: {range_text}"
            + (f"<br/>Hasta: {user_name}" if user_name else ""),
            subtitle_style,
        ),
    ]

    if not user_logs:
        story.append(Paragraph("Seçilen aralıkta kayıt bulunamadı.", subtitle_style))
    else:
        header = [
            "Tarih",
            "Kilo",
            "Tansiyon",
            "Şeker",
            "Su",
            "Nabız",
            "Not",
        ]
        rows = [header]
        for row in user_logs:
            bp = (
                f"{row.get('systolic')}/{row.get('diastolic')}"
                if row.get("systolic") and row.get("diastolic")
                else "—"
            )
            rows.append(
                [
                    _fmt_date(row.get("date")),
                    _fmt(row.get("weight"), " kg"),
                    bp,
                    _fmt(row.get("blood_glucose"), " mg/dL"),
                    _fmt(row.get("water_liters"), " L"),
                    _fmt(row.get("pulse")),
                    (row.get("notes") or "—")[:80],
                ]
            )

        table = Table(rows, colWidths=[2.2 * cm, 1.8 * cm, 2.2 * cm, 2.4 * cm, 1.6 * cm, 1.6 * cm, 4.8 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3e8ff")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#4a044e")),
                    ("FONTNAME", (0, 0), (-1, 0), font_name),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 12))
        story.append(
            Paragraph(f"Toplam {len(user_logs)} kayıt listelendi.", subtitle_style)
        )

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    buffer.seek(0)
    return buffer.read()


# Geriye dönük uyumluluk
def generate_report_content(user_logs: list[dict]) -> bytes:
    if not user_logs:
        today = date.today()
        return generate_report_pdf([], today, today)
    dates = [row.get("date") for row in user_logs if row.get("date")]
    if not dates:
        today = date.today()
        return generate_report_pdf(user_logs, today, today)
    start = date.fromisoformat(min(dates))
    end = date.fromisoformat(max(dates))
    return generate_report_pdf(user_logs, start, end)
