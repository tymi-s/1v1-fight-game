"""Generator planu treningowego (PDF) — każdy dzień na osobnej stronie.

Lustrzana wersja dokumentu Word. Cele: hipertrofia + redukcja + siła.
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

# Czcionki Unicode (obsługa polskich znaków). DejaVu nie ma wariantu oblique,
# więc kursywę mapujemy na regularny krój.
_DEJAVU = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DejaVuSans", f"{_DEJAVU}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", f"{_DEJAVU}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily(
    "DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold",
    italic="DejaVuSans", boldItalic="DejaVuSans-Bold",
)

FONT = "DejaVuSans"
FONT_B = "DejaVuSans-Bold"

NAVY = colors.HexColor("#1F3A5F")
ACCENT = colors.HexColor("#C0392B")
GREY = colors.HexColor("#555555")
HEADER_FILL = colors.HexColor("#1F3A5F")
CLUSTER_FILL = colors.HexColor("#FBE9E7")
ZEBRA_FILL = colors.HexColor("#F2F5F9")
WHITE = colors.white

styles = getSampleStyleSheet()

H_TITLE = ParagraphStyle("HTitle", parent=styles["Normal"], fontName=FONT_B,
                         fontSize=34, textColor=NAVY, alignment=TA_CENTER, leading=40)
H_SUB = ParagraphStyle("HSub", parent=styles["Normal"], fontName=FONT,
                       fontSize=15, textColor=ACCENT, alignment=TA_CENTER, leading=20)
H_SUB2 = ParagraphStyle("HSub2", parent=styles["Normal"], fontName=FONT,
                        fontSize=11, textColor=GREY, alignment=TA_CENTER, leading=16)
DAY_TAG = ParagraphStyle("DayTag", parent=styles["Normal"], fontName=FONT_B,
                         fontSize=11, textColor=ACCENT, leading=14, spaceAfter=2)
H1 = ParagraphStyle("H1", parent=styles["Normal"], fontName=FONT_B,
                    fontSize=18, textColor=NAVY, leading=22, spaceAfter=3)
H1_ACCENT = ParagraphStyle("H1a", parent=H1, textColor=ACCENT, fontSize=19)
H2 = ParagraphStyle("H2", parent=styles["Normal"], fontName=FONT_B,
                    fontSize=12.5, textColor=NAVY, leading=16, spaceBefore=8, spaceAfter=3)
SUBTITLE = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName=FONT,
                          fontSize=10, textColor=GREY, leading=13, spaceAfter=8)
BODY = ParagraphStyle("Body", parent=styles["Normal"], fontName=FONT,
                      fontSize=10, textColor=colors.black, leading=13, spaceAfter=4)
NOTE = ParagraphStyle("Note", parent=styles["Normal"], fontName=FONT,
                      fontSize=8.5, textColor=GREY, leading=11, spaceBefore=4)
CELL = ParagraphStyle("Cell", parent=styles["Normal"], fontName=FONT,
                      fontSize=8.5, leading=10.5)
CELL_L = ParagraphStyle("CellL", parent=CELL, alignment=TA_LEFT)
CELL_C = ParagraphStyle("CellC", parent=CELL, alignment=TA_CENTER)
CELL_HDR = ParagraphStyle("CellHdr", parent=styles["Normal"], fontName=FONT_B,
                          fontSize=8.5, textColor=WHITE, alignment=TA_CENTER, leading=10.5)
CELL_CLUSTER = ParagraphStyle("CellCluster", parent=CELL_L, fontName=FONT_B,
                              textColor=ACCENT)


def make_table(headers, rows, col_widths, cluster_rows=None, left_col=1):
    cluster_rows = cluster_rows or set()
    data = [[Paragraph(h, CELL_HDR) for h in headers]]
    for r_idx, row in enumerate(rows):
        is_cluster = r_idx in cluster_rows
        line = []
        for c_idx, val in enumerate(row):
            if c_idx == left_col:
                st = CELL_CLUSTER if is_cluster else CELL_L
            else:
                st = CELL_C
            line.append(Paragraph(str(val), st))
        data.append(line)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_FILL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for r_idx in range(len(rows)):
        row_pos = r_idx + 1
        if r_idx in cluster_rows:
            style.append(("BACKGROUND", (0, row_pos), (-1, row_pos), CLUSTER_FILL))
        elif r_idx % 2 == 1:
            style.append(("BACKGROUND", (0, row_pos), (-1, row_pos), ZEBRA_FILL))
    t.setStyle(TableStyle(style))
    return t


def bullets(items):
    items_fl = [ListItem(Paragraph(it, BODY), leftIndent=10) for it in items]
    return ListFlowable(items_fl, bulletType="bullet", start="•",
                        bulletColor=ACCENT, leftIndent=12)


# Szerokości kolumn dla tabel ćwiczeń (suma ~ 17.5 cm)
EX_HEADERS = ["#", "Ćwiczenie", "Serie × powt.", "Intensywność", "Przerwy"]
EX_W = [0.8 * cm, 6.6 * cm, 3.0 * cm, 4.2 * cm, 2.9 * cm]

story = []


def day_page(tag, title, subtitle, rows, cluster_rows=None, note=None, last=False):
    story.append(Paragraph(tag, DAY_TAG))
    story.append(Paragraph(title, H1))
    story.append(Paragraph(subtitle, SUBTITLE))
    story.append(make_table(EX_HEADERS, rows, EX_W, cluster_rows=cluster_rows))
    if note:
        story.append(Paragraph(note, NOTE))
    if not last:
        story.append(PageBreak())


# ---------- STRONA TYTUŁOWA ----------
story.append(Spacer(1, 2.6 * cm))
story.append(Paragraph("PLAN TRENINGOWY", H_TITLE))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Hipertrofia &bull; Redukcja tłuszczu &bull; Siła", H_SUB))
story.append(Spacer(1, 0.2 * cm))
story.append(Paragraph("Góra/Dół &times;2 + kardio  |  6 dni ruchu, 4 dni siły  |  masa ciała 80 kg", H_SUB2))
story.append(Spacer(1, 1.0 * cm))

story.append(Paragraph("Cele i założenia", H2))
story.append(make_table(["Cel", "Jak realizowany"], [
    ["Wzrost mięśni", "Każda partia 2×/tydzień, 12–18 serii/grupę, zakres 4–15 powt."],
    ["Redukcja tłuszczu", "Deficyt ~300–500 kcal + 2 biegi + wysokie białko"],
    ["Siła", "Ciężkie 4–6 powt. na głównych + cluster podciąganie"],
    ["Białko", "~160 g/dzień (2 g na 1 kg masy ciała)"],
    ["Deficyt", "Umiarkowany (~0,3–0,5 kg/tydzień), nie agresywny"],
    ["Tempo ruchu", "4 dni siłowni + 2 kardio + 1 odpoczynek"],
], [4.2 * cm, 13.3 * cm], left_col=0))

story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph("Układ tygodnia", H2))
story.append(make_table(["Dzień", "Trening", "Cel"], [
    ["Poniedziałek", "Góra A — siła", "Klatka / plecy / barki / ramiona"],
    ["Wtorek", "Dół A — siła", "Przysiad-fokus + tył uda"],
    ["Środa", "Bieg 8–10 km Z2", "Kardio / redukcja"],
    ["Czwartek", "Góra B — hipertrofia", "Objętość + CLUSTER podciąganie"],
    ["Piątek", "Dół B — hipertrofia", "Martwy/hinge + nogi objętościowo"],
    ["Sobota", "Bieg lekki 5–8 km / spacer", "Aktywna regeneracja"],
    ["Niedziela", "Odpoczynek", "Pełna regeneracja, sen 7–9 h"],
], [3.5 * cm, 6.0 * cm, 8.0 * cm], cluster_rows={3}, left_col=1))
story.append(PageBreak())

# ---------- ROZGRZEWKA ----------
story.append(Paragraph("ROZGRZEWKA", H1_ACCENT))
story.append(Paragraph("Wykonuj przed KAŻDYM treningiem siłowym (~10–15 min). To inwestycja w jakość serii roboczych i ochronę przed kontuzją.", SUBTITLE))

story.append(Paragraph("1. Ogólna (5 min)", H2))
story.append(bullets(["Rower stacjonarny / bieżnia / wiosło — spokojne tempo, podniesienie tętna i temperatury ciała."]))

story.append(Paragraph("2. Mobilność dynamiczna (3–5 min)", H2))
story.append(bullets([
    "Krążenia ramion i bioder — po 10 w każdą stronę.",
    "Przysiady z masą ciała — 10 powt. (pełny zakres).",
    "„World's greatest stretch” — 5 na stronę.",
    "Band pull-apart (guma) — 15 powt.",
]))

story.append(Paragraph("3. Aktywacja (2–3 min)", H2))
story.append(bullets([
    "Dead bug — 8 na stronę (core).",
    "Glute bridge — 10 powt. (pośladki, przed dniem nóg).",
    "Face pull lekki gumą — 15 powt. (barki, przed dniem góry).",
]))

story.append(Paragraph("4. Ramping pierwszego ćwiczenia", H2))
story.append(Paragraph("Rozgrzej się progresywnie do ciężaru roboczego pierwszego ćwiczenia dnia:", BODY))
story.append(make_table(["Krok", "Obciążenie", "Powtórzenia"], [
    ["1", "Pusta sztanga", "5"],
    ["2", "~40% ciężaru roboczego", "3"],
    ["3", "~60% ciężaru roboczego", "2"],
    ["4", "~75% ciężaru roboczego", "1"],
    ["5", "Seria robocza", "wg planu"],
], [2.5 * cm, 9.0 * cm, 6.0 * cm], left_col=1))
story.append(Paragraph("Przed podciąganiem z obciążeniem: 2×3–5 powt. bez dodatkowego ciężaru + 1×2 powt. z ~50% docelowego dodatku.", NOTE))
story.append(PageBreak())

# ---------- DNI ----------
day_page(
    "DZIEŃ 1 / PONIEDZIAŁEK",
    "GÓRA A — Siła",
    "Klatka, plecy, barki, biceps, triceps. Fokus na ciężkie zakresy (4–6 powt.) dla rozwoju siły.",
    [
        ["1", "Wyciskanie leżąc (sztanga)", "4 × 4–6", "80–85% / RPE 8", "3 min"],
        ["2", "Wiosłowanie sztangą / Pendlay row", "4 × 5–6", "RPE 8", "2–3 min"],
        ["3", "OHP — wyciskanie żołnierskie", "3 × 6–8", "RPE 8", "2–3 min"],
        ["4", "Podciąganie z obciążeniem", "3 × 5–6", "RPE 8", "2–3 min"],
        ["5", "Prostowanie tricepsa (wyciąg)", "3 × 8–10", "RPE 8–9", "90 s"],
        ["6", "Uginanie bicepsa (sztanga/hantle)", "3 × 8–10", "RPE 8–9", "90 s"],
    ],
    note="Nie trenuj do upadku na ćwiczeniach 1–4. Ostatnie serie akcesoriów (5–6) mogą być bliżej upadku (RPE 9).",
)

day_page(
    "DZIEŃ 2 / WTOREK",
    "DÓŁ A — Siła (przysiad-fokus)",
    "Czworogłowe, pośladki, tył uda, łydki, core. Ciężki przysiad jako główny bodziec siłowy.",
    [
        ["1", "Przysiad ze sztangą", "4 × 4–6", "80% / RPE 8", "3 min"],
        ["2", "Martwy ciąg rumuński (RDL)", "3 × 6–8", "RPE 8", "2–3 min"],
        ["3", "Leg press / hack squat", "3 × 8–10", "RPE 8", "2 min"],
        ["4", "Uginanie nóg leżąc (dwugłowe)", "3 × 10–12", "RPE 8–9", "90 s"],
        ["5", "Wspięcia na palce (łydki)", "4 × 10–12", "RPE 9", "90 s"],
        ["6", "Core: Pallof press / rollout", "3 × 8–10", "RPE 8", "90 s"],
    ],
    note="Ciężkie nogi wtorek + piątek. Mocniejszy bieg dopiero w środę (~48 h regeneracji).",
)

# Środa — kardio
story.append(Paragraph("DZIEŃ 3 / ŚRODA", DAY_TAG))
story.append(Paragraph("KARDIO — Bieg", H1))
story.append(Paragraph("Trening tlenowy dla redukcji tłuszczu i kondycji. Bez rujnowania regeneracji nóg.", SUBTITLE))
story.append(make_table(["Element", "Wykonanie"], [
    ["Dystans", "8–10 km"],
    ["Tempo / strefa", "Strefa 2 (Z2) — tempo rozmowowe, ~65–75% max HR"],
    ["Rozgrzewka", "5 min marsz / trucht + 4×20 s przyspieszenia"],
    ["Schłodzenie", "5 min spokojny marsz + rozciąganie łydek i bioder"],
    ["Cel", "Wydatek energetyczny + baza tlenowa, NIE interwały"],
], [4.2 * cm, 13.3 * cm], left_col=0))
story.append(Paragraph("Jeśli po wtorkowych nogach czujesz się rozbity — skróć do 6–8 km. Bieg Z2 nie konkuruje z regeneracją siłową tak jak sprinty/HIIT.", NOTE))
story.append(PageBreak())

day_page(
    "DZIEŃ 4 / CZWARTEK",
    "GÓRA B — Hipertrofia + CLUSTER",
    "Objętość dla wzrostu mięśni + cluster podciąganie jako bodziec siłowy (Twój priorytet).",
    [
        ["1", "PODCIĄGANIE Z OBCIĄŻENIEM — CLUSTER", "3 klastry × 5×1", "~80% dodatku (+16 kg)", "20–30 s / 3 min"],
        ["2", "Wyciskanie hantli na skosie", "4 × 8–10", "RPE 8", "2 min"],
        ["3", "Wiosłowanie na wyciągu / chest-supported", "4 × 8–12", "RPE 8–9", "2 min"],
        ["4", "Rozpiętki / cable fly", "3 × 12–15", "RPE 9", "90 s"],
        ["5", "Lateral raise (barki boczne)", "4 × 12–15", "RPE 9", "60–90 s"],
        ["6", "Uginanie młotkowe + face pull (superset)", "3 × 12–15", "RPE 8–9", "60–90 s"],
    ],
    cluster_rows={0},
    note="CLUSTER: 1 powt. → zejście → 20–30 s przerwy → 1 powt. → … ×5 = 1 klaster. Razem 3 klastry, między nimi 3 min. Każde powtórzenie pełny zakres.",
)

day_page(
    "DZIEŃ 5 / PIĄTEK",
    "DÓŁ B — Hipertrofia (hinge-fokus)",
    "Tył łańcucha, pośladki, czworogłowe, łydki, core. Martwy ciąg technicznie (nie na maksa w deficycie).",
    [
        ["1", "Martwy ciąg", "3 × 5", "80% / RPE 8", "3 min"],
        ["2", "Hip thrust (pośladki)", "3 × 8–10", "RPE 8–9", "2 min"],
        ["3", "Wykroki / przysiad bułgarski", "3 × 8–10 / noga", "RPE 8", "90–120 s"],
        ["4", "Prostowanie nóg (czworogłowe)", "3 × 12–15", "RPE 9", "90 s"],
        ["5", "Wspięcia na palce (inny kąt)", "4 × 12–15", "RPE 9", "60–90 s"],
        ["6", "Core: hanging leg raise", "3 × 10–12", "RPE 8", "60–90 s"],
    ],
    note="W deficycie martwy ciąg trzymaj technicznie — jakość, nie ego. To ostatni ciężki dzień przed weekendem.",
)

# Sobota
story.append(Paragraph("DZIEŃ 6 / SOBOTA", DAY_TAG))
story.append(Paragraph("KARDIO LEKKIE — Regeneracja aktywna", H1))
story.append(Paragraph("Spokojny wysiłek wspierający regenerację i dodatkowy wydatek energetyczny.", SUBTITLE))
story.append(make_table(["Element", "Wykonanie"], [
    ["Opcja A", "Bieg spokojny 5–8 km (wolniej niż w środę)"],
    ["Opcja B", "Marsz / spacer 45–60 min (jeśli zmęczenie)"],
    ["Tempo", "Bardzo lekkie — masz się zregenerować, nie zmęczyć"],
    ["Cel", "Krążenie, redukcja, mobilność — bez obciążania nóg"],
], [4.2 * cm, 13.3 * cm], left_col=0))
story.append(Paragraph("Słuchaj ciała: jeśli tydzień był ciężki lub sen słaby, wybierz spacer zamiast biegu.", NOTE))
story.append(PageBreak())

# Niedziela
story.append(Paragraph("DZIEŃ 7 / NIEDZIELA", DAY_TAG))
story.append(Paragraph("ODPOCZYNEK", H1))
story.append(Paragraph("Pełna regeneracja — kluczowa dla wzrostu mięśni i siły, zwłaszcza w deficycie kalorycznym.", SUBTITLE))
story.append(make_table(["Priorytet", "Zalecenie"], [
    ["Sen", "7–9 godzin — najważniejszy czynnik regeneracji"],
    ["Aktywność", "Brak treningu; ewentualnie lekki spacer"],
    ["Odżywianie", "Trzymaj białko ~160 g nawet w dniu wolnym"],
    ["Regeneracja", "Rozciąganie, rolowanie, nawodnienie"],
], [4.2 * cm, 13.3 * cm], left_col=0))
story.append(PageBreak())

# ---------- CLUSTER ----------
story.append(Paragraph("CLUSTER SETS — instrukcja", H1_ACCENT))
story.append(Paragraph("Metoda dla rozwoju siły: pojedyncze powtórzenia z krótkimi przerwami wewnątrz serii, przy wysokiej intensywności bez spadku jakości.", SUBTITLE))

story.append(Paragraph("Podciąganie z obciążeniem (stały element)", H2))
story.append(bullets([
    "Obciążenie: ~80% 1RM dodatku. Przy maksie +20 kg na łańcuchu → rób +16 kg.",
    "Wykonanie: 1 powtórzenie → kontrolowane zejście → 20–30 s przerwy → kolejne 1 powtórzenie.",
    "Powtórz do 5 pojedynczych powtórzeń = 1 klaster.",
    "Wykonaj 3 klastry, między klastrami 3 minuty przerwy.",
    "Każde powtórzenie: pełny zakres ruchu, kontrolowany negatyw.",
]))

story.append(Paragraph("Które ćwiczenia nadają się na cluster", H2))
story.append(Paragraph("Cluster najlepiej działa na ćwiczeniach WIELOSTAWOWYCH (dużo mięśni naraz), z łatwym resetem między powtórzeniami. Na izolacjach nie ma sensu.", BODY))
story.append(make_table(["Ćwiczenie", "Cluster?", "Dlaczego"], [
    ["Podciąganie z obciążeniem", "TAK — stały element", "Twój priorytet, łatwy reset, wysoka intensywność"],
    ["Wyciskanie leżąc", "TAK (opcjonalnie)", "Wielostawowe, łatwy reset na stojakach"],
    ["OHP / żołnierskie", "TAK (opcjonalnie)", "Wielostawowe, cluster utrzymuje jakość"],
    ["Dipy z obciążeniem", "TAK (opcjonalnie)", "Krótki ROM, łatwa pauza"],
    ["Przysiad", "Raczej NIE", "Setup i zmęczenie core > korzyść; lepiej klasyczne serie"],
    ["Martwy ciąg", "NIE", "Każde powt. = pełny setup; lepiej klasyczne single/double"],
    ["Wiosłowanie", "NIE", "Nie max-effort; klasyczne serie wystarczą"],
    ["Izolacje (biceps, łydki, barki)", "NIE", "Za mała korzyść dla siły"],
], [5.2 * cm, 4.0 * cm, 8.3 * cm], left_col=0))
story.append(Paragraph("W tym planie (redukcja + hipertrofia) cluster stosujemy głównie na podciąganiu. Bench/OHP/dipy możesz dodać jako cluster później, jeśli chcesz mocniej dociągnąć siłę pchania.", NOTE))
story.append(PageBreak())

# ---------- PROGRESJA + DIETA ----------
story.append(Paragraph("PROGRESJA, REGENERACJA, DIETA", H1_ACCENT))

story.append(Paragraph("Kiedy zwiększać ciężar", H2))
story.append(make_table(["Sytuacja", "Działanie"], [
    ["Wszystkie serie w zakresie powt., RPE ≤ 8", "+2,5 kg (sztanga) lub +1–2 powt. (hantle)"],
    ["RPE 9–10, ledwo domykasz zakres", "Zostań przy tym samym ciężarze"],
    ["Cluster podciąganie 3×5×1 @+16 kg łatwe (RPE ≤8)", "+1–2 kg na łańcuchu"],
    ["2 tygodnie bez postępu", "Sprawdź sen / kalorie / białko; rozważ deload"],
    ["Co 6–8 tygodni", "Deload: −40% objętości, −10% ciężaru, 1 tydzień"],
], [8.7 * cm, 8.8 * cm, ], left_col=0))

story.append(Paragraph("Zasady w deficycie kalorycznym", H2))
story.append(bullets([
    "Siła może rosnąć wolniej — utrzymanie ciężarów + drobne PR to już sukces.",
    "Trzymaj INTENSYWNOŚĆ (ciężar); jeśli brakuje regeneracji, tnij raczej OBJĘTOŚĆ (serie).",
    "Priorytet: sen 7–9 h, białko 2 g/kg, umiarkowany deficyt.",
]))

story.append(Paragraph("Dieta — minimum, które musi grać", H2))
story.append(make_table(["Parametr", "Cel"], [
    ["Białko", "~160 g/dzień (2 g na 1 kg masy ciała)"],
    ["Deficyt", "~300–500 kcal/dzień (nie więcej)"],
    ["Tempo redukcji", "~0,3–0,5 kg/tydzień"],
    ["Nawodnienie", "~30–35 ml/kg masy ciała dziennie"],
], [5.0 * cm, 12.5 * cm], left_col=0))

story.append(Paragraph("Dlaczego ten plan maksymalizuje Twoje cele", H2))
story.append(bullets([
    "MIĘŚNIE: każda partia 2×/tydzień, 12–18 serii/grupę, zakresy 4–15 — pełne spektrum bodźców.",
    "SIŁA: ciężkie 4–6 powt. na bench/przysiad/martwy/OHP + cluster podciąganie.",
    "TŁUSZCZ: 2 biegi + deficyt + wysokie białko.",
    "REGENERACJA: tylko 4 dni siły — w deficycie realnie się zregenerujesz (lepsze niż 6× średnio).",
]))


def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GREY)
    canvas.drawCentredString(A4[0] / 2.0, 1.0 * cm, str(doc_.page))
    canvas.restoreState()


doc = BaseDocTemplate("Plan_treningowy.pdf", pagesize=A4,
                      topMargin=1.4 * cm, bottomMargin=1.6 * cm,
                      leftMargin=1.8 * cm, rightMargin=1.8 * cm)
frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
doc.build(story)
print("Zapisano: Plan_treningowy.pdf")
