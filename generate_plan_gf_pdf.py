"""Generator planu treningowego (PDF) — hipertrofia: pośladki + plecy, redukcja.

Każdy dzień na osobnej stronie. Polskie znaki (font DejaVu).
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import plan_gf_data as P

# --- Czcionki Unicode (polskie znaki) ---
_DEJAVU = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DejaVuSans", f"{_DEJAVU}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", f"{_DEJAVU}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily(
    "DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold",
    italic="DejaVuSans", boldItalic="DejaVuSans-Bold",
)
FONT = "DejaVuSans"
FONT_B = "DejaVuSans-Bold"

# --- Paleta (kobieca, ale czytelna) ---
PLUM = colors.HexColor("#6C2B5A")     # główny (śliwka)
ACCENT = colors.HexColor("#B5347E")   # różowy akcent
GREY = colors.HexColor("#555555")
HEADER_FILL = colors.HexColor("#6C2B5A")
GLUTE_FILL = colors.HexColor("#F7E9F2")
ZEBRA_FILL = colors.HexColor("#F5F2F7")
WHITE = colors.white

styles = getSampleStyleSheet()
H_TITLE = ParagraphStyle("HTitle", parent=styles["Normal"], fontName=FONT_B, fontSize=32, textColor=PLUM, alignment=TA_CENTER, leading=38)
H_SUB = ParagraphStyle("HSub", parent=styles["Normal"], fontName=FONT, fontSize=15, textColor=ACCENT, alignment=TA_CENTER, leading=20)
H_SUB2 = ParagraphStyle("HSub2", parent=styles["Normal"], fontName=FONT, fontSize=11, textColor=GREY, alignment=TA_CENTER, leading=16)
DAY_TAG = ParagraphStyle("DayTag", parent=styles["Normal"], fontName=FONT_B, fontSize=11, textColor=ACCENT, leading=14, spaceAfter=2)
H1 = ParagraphStyle("H1", parent=styles["Normal"], fontName=FONT_B, fontSize=18, textColor=PLUM, leading=22, spaceAfter=3)
H1_ACCENT = ParagraphStyle("H1a", parent=H1, textColor=ACCENT, fontSize=19)
H2 = ParagraphStyle("H2", parent=styles["Normal"], fontName=FONT_B, fontSize=12.5, textColor=PLUM, leading=16, spaceBefore=8, spaceAfter=3)
SUBTITLE = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName=FONT, fontSize=10, textColor=GREY, leading=13, spaceAfter=8)
BODY = ParagraphStyle("Body", parent=styles["Normal"], fontName=FONT, fontSize=10, textColor=colors.black, leading=13, spaceAfter=4)
NOTE = ParagraphStyle("Note", parent=styles["Normal"], fontName=FONT, fontSize=8.5, textColor=GREY, leading=11, spaceBefore=4)
CELL = ParagraphStyle("Cell", parent=styles["Normal"], fontName=FONT, fontSize=8.5, leading=10.5)
CELL_L = ParagraphStyle("CellL", parent=CELL, alignment=TA_LEFT)
CELL_C = ParagraphStyle("CellC", parent=CELL, alignment=TA_CENTER)
CELL_HDR = ParagraphStyle("CellHdr", parent=styles["Normal"], fontName=FONT_B, fontSize=8.5, textColor=WHITE, alignment=TA_CENTER, leading=10.5)


def make_table(headers, rows, col_widths, highlight_rows=None, left_col=1):
    highlight_rows = highlight_rows or set()
    data = [[Paragraph(h, CELL_HDR) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(v), CELL_L if i == left_col else CELL_C) for i, v in enumerate(r)])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_FILL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D9CCD6")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for r_idx in range(len(rows)):
        pos = r_idx + 1
        if r_idx in highlight_rows:
            style.append(("BACKGROUND", (0, pos), (-1, pos), GLUTE_FILL))
        elif r_idx % 2 == 1:
            style.append(("BACKGROUND", (0, pos), (-1, pos), ZEBRA_FILL))
    t.setStyle(TableStyle(style))
    return t


def bullets(items):
    return ListFlowable([ListItem(Paragraph(it, BODY), leftIndent=10) for it in items],
                        bulletType="bullet", start="•", bulletColor=ACCENT, leftIndent=12)


EX_HEADERS = ["#", "Ćwiczenie", "Serie × powt.", "Intensywność", "Przerwy"]
EX_W = [0.8 * cm, 6.4 * cm, 2.7 * cm, 4.7 * cm, 2.9 * cm]

story = []


def day_page(day, last=False):
    story.append(Paragraph(day["tag"], DAY_TAG))
    story.append(Paragraph(day["title"], H1))
    story.append(Paragraph(day["subtitle"], SUBTITLE))
    if day["type"] == "silownia":
        rows = []
        for i, (name, nsets, reps, inten, rest) in enumerate(day["exercises"], start=1):
            rows.append([str(i), name, f"{nsets} × {reps}", inten, rest])
        story.append(make_table(EX_HEADERS, rows, EX_W))
        if day.get("note"):
            story.append(Paragraph(day["note"], NOTE))
    else:
        story.append(make_table(["Element", "Wykonanie"],
                                [["Plan", day["info"]]],
                                [3.2 * cm, 14.3 * cm], left_col=0))
    if not last:
        story.append(PageBreak())


# ---------- STRONA TYTUŁOWA ----------
story.append(Spacer(1, 2.2 * cm))
story.append(Paragraph("PLAN TRENINGOWY", H_TITLE))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Hipertrofia: pośladki &amp; plecy &bull; Redukcja tłuszczu", H_SUB))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph("5 dni ruchu (4 siłownia + cardio) &bull; minimalny akcent na uda", H_SUB2))
story.append(Spacer(1, 0.9 * cm))

story.append(Paragraph("Cele i założenia", H2))
story.append(make_table(["Cel", "Jak realizowany"], [[c, d] for c, d in P.CELE],
                        [5.0 * cm, 12.5 * cm], left_col=0))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Układ tygodnia", H2))
story.append(make_table(["Dzień", "Trening", "Cel"],
                        [[a, b, c] for a, b, c in P.WEEK_OVERVIEW],
                        [3.2 * cm, 6.5 * cm, 7.8 * cm], left_col=1))
story.append(PageBreak())

# ---------- WAŻNE: JAK TO DZIAŁA ----------
story.append(Paragraph("WAŻNE — jak to działa", H1_ACCENT))
story.append(Paragraph("Zanim zaczniesz, przeczytaj — to decyduje o efektach.", SUBTITLE))

story.append(Paragraph("Chudnięcie z brzucha i dolnych pleców", H2))
story.append(bullets([
    "Nie da się schudnąć punktowo. Tłuszcz z brzucha i dolnych pleców schodzi wtedy, gdy chudniesz z CAŁEGO ciała — czyli przy deficycie kalorycznym.",
    "Ćwiczenia brzucha i pleców budują mięśnie i poprawiają sylwetkę, ale same nie „spalają” tłuszczu w tym miejscu.",
    "O redukcji decyduje głównie dieta (deficyt + białko), a cardio i trening ją wspierają.",
]))

story.append(Paragraph("Pośladki i plecy TAK, uda (przód) minimalnie", H2))
story.append(bullets([
    "Trening decyduje, KTÓRE mięśnie rosną. Dlatego stawiamy na ruchy biodro-dominujące (hip thrust, RDL, odwodzenie, back extension, kickback), które budują pośladek bez mocnego angażowania przodu uda.",
    "Świadomie usunięte: prostowanie nóg (czwórki) i ciężki leg press — najmocniej rozbudowują czworogłowe (przód uda).",
    "Step up i RDL z wychyleniem do przodu i naciskiem na piętę = akcent na pośladek, nie na udo.",
    "Plecy budujemy częstotliwością i różnymi kątami ciągnięcia (ściąganie, wiosłowania, face pull).",
]))

story.append(Paragraph("Twoje ulubione ćwiczenia zostają", H2))
story.append(bullets([
    "Biceps hantlami, triceps na lince, face pull na lince, hip thrust na maszynie, odwodzenie na maszynie, step up na lince — wszystkie są w planie.",
]))
story.append(PageBreak())

# ---------- ROZGRZEWKA ----------
story.append(Paragraph("ROZGRZEWKA", H1_ACCENT))
story.append(Paragraph("Do wykonania przed KAŻDYM treningiem siłowym (~10 min).", SUBTITLE))

story.append(Paragraph("1. Ogólna (5 min)", H2))
story.append(bullets(["Rower / orbitrek / bieżnia — spokojne tempo, rozgrzanie ciała."]))

story.append(Paragraph("2. Aktywacja przed dniem POŚLADKÓW (pon./czw.)", H2))
story.append(bullets([
    "Glute bridge z gumą — 15 powt.",
    "Odwodzenie z gumą (chodzenie w bok) — 10 kroków / stronę.",
    "Hip thrust z samą masą / lekko — 15 powt. (rozgrzewkowo).",
]))

story.append(Paragraph("3. Aktywacja przed dniem GÓRY (wt./sob.)", H2))
story.append(bullets([
    "Band pull-apart (guma) — 15 powt.",
    "Krążenia ramion — 10 w każdą stronę.",
    "Lekka seria pierwszego ćwiczenia (50% ciężaru) — 10 powt.",
]))

story.append(Paragraph("4. Ramping pierwszego ćwiczenia", H2))
story.append(Paragraph("Przed pierwszym ćwiczeniem dnia zrób 1–2 lżejsze serie (ok. 50–70% docelowego ciężaru), by przygotować mięśnie i technikę.", BODY))
story.append(PageBreak())

# ---------- DNI ----------
for i, day in enumerate(P.DAYS_ORDER):
    day_page(day, last=False)

# ---------- PROGRESJA, DIETA ----------
story.append(Paragraph("PROGRESJA, DIETA, REGENERACJA", H1_ACCENT))

story.append(Paragraph("Kiedy zwiększać ciężar", H2))
story.append(make_table(["Sytuacja", "Działanie"], [
    ["Wszystkie serie w górnym zakresie powt., RPE ≤ 8", "+ mały krok ciężaru (np. +2,5 kg maszyna / +1–2 kg hantle)"],
    ["Zakres powt. jeszcze niepełny", "Zostań przy ciężarze, dokładaj powtórzenia"],
    ["RPE 9–10, technika się psuje", "Utrzymanie lub zmniejszenie ciężaru"],
    ["Co 6–8 tygodni", "Lżejszy tydzień (deload): −30–40% objętości"],
], [8.7 * cm, 8.8 * cm], left_col=0))

story.append(Paragraph("Dieta — najważniejsza pod redukcję", H2))
story.append(make_table(["Parametr", "Cel"], [
    ["Białko", "1,6–2,2 g / kg masy ciała (np. 60 kg → ~100–130 g)"],
    ["Deficyt", "Umiarkowany (~300–500 kcal/dzień)"],
    ["Tempo chudnięcia", "~0,3–0,5 kg / tydzień (bez utraty mięśni)"],
    ["Nawodnienie", "~30–35 ml / kg masy ciała dziennie"],
    ["Warzywa i błonnik", "Dużo — sytość przy niższych kaloriach"],
], [3.6 * cm, 13.9 * cm], left_col=0))
story.append(Paragraph("Masę ciała podaj, aby dokładnie policzyć białko — powyżej przykład dla 60 kg.", NOTE))

story.append(Paragraph("Dlaczego ten plan pasuje do celów", H2))
story.append(bullets([
    "Pośladki 2×/tydzień z pełną objętością (hip thrust, odwodzenie, RDL, back extension) = szybszy wzrost.",
    "Plecy 2–3×/tydzień z różnych kątów = grubość i szerokość bez przerostu ud.",
    "Bez prostowania nóg i ciężkiego leg press = uda (przód) rosną minimalnie.",
    "Cardio + deficyt + białko = redukcja tłuszczu z całego ciała (w tym brzuch i dolne plecy).",
    "Zakresy 8–15 powt. i RPE 8 = klasyczna hipertrofia bez zbędnego zajeżdżania.",
]))


def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GREY)
    canvas.drawCentredString(A4[0] / 2.0, 1.0 * cm, str(doc_.page))
    canvas.restoreState()


doc = BaseDocTemplate("Plan_treningowy_dziewczyna.pdf", pagesize=A4,
                      topMargin=1.4 * cm, bottomMargin=1.6 * cm,
                      leftMargin=1.8 * cm, rightMargin=1.8 * cm)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
doc.build(story)
print("Zapisano: Plan_treningowy_dziewczyna.pdf")
