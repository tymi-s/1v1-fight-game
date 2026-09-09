"""Generator planu treningowego (Word .docx).

Tworzy estetyczny dokument: rozgrzewka na początku, każdy dzień treningowy
na osobnej stronie, dane w tabelach. Cele: hipertrofia + redukcja + siła.
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ----- Paleta kolorów -----
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT = RGBColor(0xC0, 0x39, 0x2B)   # czerwony akcent (cluster / ważne)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0x55, 0x55, 0x55)

HEADER_FILL = "1F3A5F"   # navy
CLUSTER_FILL = "FBE9E7"  # jasny czerwony (wiersze cluster)
ZEBRA_FILL = "F2F5F9"    # jasny szary


def set_cell_background(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tc_pr.append(shd)


def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tc_pr = cell._tc.get_or_add_tcPr()
    margins = OxmlElement("w:tcMar")
    for tag, val in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        node = OxmlElement(f"w:{tag}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        margins.append(node)
    tc_pr.append(margins)


def style_cell_text(cell, bold=False, color=None, size=10, align=None):
    for p in cell.paragraphs:
        if align is not None:
            p.alignment = align
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        for run in p.runs:
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.name = "Calibri"
            if color is not None:
                run.font.color.rgb = color


def add_heading(doc, text, size=20, color=NAVY, space_before=0, space_after=8):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return p


def add_subtitle(doc, text, color=GREY, size=11):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.italic = True
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return p


def add_para(doc, text, size=10.5, bold=False, color=None, space_after=6, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "Calibri"
    if color is not None:
        run.font.color.rgb = color
    return p


def add_bullets(doc, items, size=10.5):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(it)
        run.font.size = Pt(size)
        run.font.name = "Calibri"


def add_table(doc, headers, rows, widths=None, cluster_rows=None):
    """rows: lista list. cluster_rows: zbiór indeksów wierszy do podświetlenia."""
    cluster_rows = cluster_rows or set()
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    table.autofit = False

    # Nagłówek
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        set_cell_background(hdr[i], HEADER_FILL)
        set_cell_margins(hdr[i])
        style_cell_text(hdr[i], bold=True, color=WHITE, size=10,
                        align=WD_ALIGN_PARAGRAPH.CENTER)

    # Wiersze
    for r_idx, row in enumerate(rows):
        cells = table.add_row().cells
        is_cluster = r_idx in cluster_rows
        for c_idx, val in enumerate(row):
            cells[c_idx].text = str(val)
            set_cell_margins(cells[c_idx])
            if is_cluster:
                set_cell_background(cells[c_idx], CLUSTER_FILL)
            elif r_idx % 2 == 1:
                set_cell_background(cells[c_idx], ZEBRA_FILL)
            align = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
            style_cell_text(cells[c_idx], bold=(c_idx == 1 and is_cluster),
                            color=(ACCENT if is_cluster and c_idx == 1 else None),
                            size=9.5, align=align)

    if widths:
        for row in table.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
    return table


def add_page_break(doc):
    doc.add_page_break()


def day_page(doc, tag, title, subtitle, headers, rows, widths, cluster_rows=None,
             note=None):
    """Jedna strona = jeden dzień."""
    # kolorowy pasek dnia
    bar = doc.add_paragraph()
    bar.paragraph_format.space_after = Pt(2)
    run = bar.add_run(tag)
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = ACCENT
    run.font.name = "Calibri"

    add_heading(doc, title, size=19, color=NAVY, space_after=2)
    add_subtitle(doc, subtitle)
    add_table(doc, headers, rows, widths=widths, cluster_rows=cluster_rows)
    if note:
        add_para(doc, note, size=9.5, color=GREY, space_after=0)


# ============================================================
# BUDOWA DOKUMENTU
# ============================================================
doc = Document()

# Marginesy
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

# Domyślna czcionka
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)

EX_HEADERS = ["#", "Ćwiczenie", "Serie × powt.", "Intensywność", "Przerwy"]
EX_WIDTHS = [0.4, 3.0, 1.4, 1.7, 1.1]

# ---------- STRONA TYTUŁOWA ----------
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Pt(90)
run = title.add_run("PLAN TRENINGOWY")
run.font.size = Pt(36)
run.font.bold = True
run.font.color.rgb = NAVY
run.font.name = "Calibri"

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = sub.add_run("Hipertrofia • Redukcja tłuszczu • Siła")
run.font.size = Pt(16)
run.font.color.rgb = ACCENT
run.font.name = "Calibri"

sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub2.paragraph_format.space_after = Pt(30)
run = sub2.add_run("Góra/Dół ×2 + kardio  |  6 dni ruchu, 4 dni siły  |  masa ciała 80 kg")
run.font.size = Pt(12)
run.font.color.rgb = GREY
run.font.name = "Calibri"

# Tabela celów
add_heading(doc, "Cele i założenia", size=15, space_before=10)
goals = [
    ["Wzrost mięśni", "Każda partia 2×/tydzień, 12–18 serii/grupę, zakres 4–15 powt."],
    ["Redukcja tłuszczu", "Deficyt ~300–500 kcal + 2 biegi + wysokie białko"],
    ["Siła", "Ciężkie 4–6 powt. na głównych + cluster podciąganie"],
    ["Białko", "~160 g/dzień (2 g na 1 kg masy ciała)"],
    ["Deficyt", "Umiarkowany (~0,3–0,5 kg/tydzień), nie agresywny"],
    ["Tempo ruchu", "6 dni ruchu / tydzień, 4 dni siłowni + 2 kardio + 1 odpoczynek"],
]
add_table(doc, ["Cel", "Jak realizowany"], goals, widths=[1.8, 5.7])

add_heading(doc, "Układ tygodnia", size=15, space_before=14)
week = [
    ["Poniedziałek", "Góra A — siła", "Klatka / plecy / barki / ramiona"],
    ["Wtorek", "Dół A — siła", "Przysiad-fokus + tył uda"],
    ["Środa", "Bieg 8–10 km Z2", "Kardio / redukcja"],
    ["Czwartek", "Góra B — hipertrofia", "Objętość + CLUSTER podciąganie"],
    ["Piątek", "Dół B — hipertrofia", "Martwy/hinge + nogi objętościowo"],
    ["Sobota", "Bieg lekki 5–8 km / spacer", "Aktywna regeneracja"],
    ["Niedziela", "Odpoczynek", "Pełna regeneracja, sen 7–9 h"],
]
add_table(doc, ["Dzień", "Trening", "Cel"], week,
          widths=[1.5, 2.6, 3.4],
          cluster_rows={3})

add_page_break(doc)

# ---------- ROZGRZEWKA (na początku) ----------
add_heading(doc, "ROZGRZEWKA", size=22, color=ACCENT)
add_subtitle(doc, "Wykonuj przed KAŻDYM treningiem siłowym (~10–15 min). Rozgrzewka to inwestycja w jakość serii roboczych i ochronę przed kontuzją.")

add_heading(doc, "1. Ogólna (5 min)", size=13)
add_bullets(doc, [
    "Rower stacjonarny / bieżnia / wiosło — spokojne tempo, podniesienie tętna i temperatury ciała.",
])

add_heading(doc, "2. Mobilność dynamiczna (3–5 min)", size=13)
add_bullets(doc, [
    "Krążenia ramion i bioder — po 10 w każdą stronę.",
    "Przysiady z masą ciała — 10 powt. (pełny zakres).",
    "„World's greatest stretch” — 5 na stronę.",
    "Band pull-apart (guma) — 15 powt.",
])

add_heading(doc, "3. Aktywacja (2–3 min)", size=13)
add_bullets(doc, [
    "Dead bug — 8 na stronę (core).",
    "Glute bridge — 10 powt. (pośladki, przed dniem nóg).",
    "Face pull lekki gumą — 15 powt. (barki, przed dniem góry).",
])

add_heading(doc, "4. Ramping pierwszego ćwiczenia", size=13)
add_para(doc, "Rozgrzej się progresywnie do ciężaru roboczego pierwszego ćwiczenia dnia:")
add_table(doc, ["Krok", "Obciążenie", "Powtórzenia"], [
    ["1", "Pusta sztanga", "5"],
    ["2", "~40% ciężaru roboczego", "3"],
    ["3", "~60% ciężaru roboczego", "2"],
    ["4", "~75% ciężaru roboczego", "1"],
    ["5", "Seria robocza", "wg planu"],
], widths=[1.0, 3.5, 3.0])

add_para(doc, "Przed podciąganiem z obciążeniem: 2×3–5 powt. bez dodatkowego ciężaru + 1×2 powt. z ~50% docelowego dodatku.",
         size=9.5, color=GREY, space_after=0)

add_page_break(doc)

# ---------- PONIEDZIAŁEK ----------
day_page(
    doc,
    "DZIEŃ 1 / PONIEDZIAŁEK",
    "GÓRA A — Siła",
    "Klatka, plecy, barki, biceps, triceps. Fokus na ciężkie zakresy (4–6 powt.) dla rozwoju siły.",
    EX_HEADERS,
    [
        ["1", "Wyciskanie leżąc (sztanga)", "4 × 4–6", "80–85% / RPE 8", "3 min"],
        ["2", "Wiosłowanie sztangą / Pendlay row", "4 × 5–6", "RPE 8", "2–3 min"],
        ["3", "OHP — wyciskanie żołnierskie", "3 × 6–8", "RPE 8", "2–3 min"],
        ["4", "Podciąganie z obciążeniem", "3 × 5–6", "RPE 8", "2–3 min"],
        ["5", "Prostowanie tricepsa (wyciąg)", "3 × 8–10", "RPE 8–9", "90 s"],
        ["6", "Uginanie bicepsa (sztanga/hantle)", "3 × 8–10", "RPE 8–9", "90 s"],
    ],
    EX_WIDTHS,
    note="Nie trenuj do upadku na ćwiczeniach 1–4. Ostatnie serie akcesoriów (5–6) mogą być bliżej upadku (RPE 9).",
)

add_page_break(doc)

# ---------- WTOREK ----------
day_page(
    doc,
    "DZIEŃ 2 / WTOREK",
    "DÓŁ A — Siła (przysiad-fokus)",
    "Czworogłowe, pośladki, tył uda, łydki, core. Ciężki przysiad jako główny bodziec siłowy.",
    EX_HEADERS,
    [
        ["1", "Przysiad ze sztangą", "4 × 4–6", "80% / RPE 8", "3 min"],
        ["2", "Martwy ciąg rumuński (RDL)", "3 × 6–8", "RPE 8", "2–3 min"],
        ["3", "Leg press / hack squat", "3 × 8–10", "RPE 8", "2 min"],
        ["4", "Uginanie nóg leżąc (dwugłowe)", "3 × 10–12", "RPE 8–9", "90 s"],
        ["5", "Wspięcia na palce (łydki)", "4 × 10–12", "RPE 9", "90 s"],
        ["6", "Core: Pallof press / rollout", "3 × 8–10", "RPE 8", "90 s"],
    ],
    EX_WIDTHS,
    note="Ciężkie nogi wtorek + piątek. Mocniejszy bieg dopiero w środę (~48 h regeneracji).",
)

add_page_break(doc)

# ---------- ŚRODA ----------
bar = doc.add_paragraph()
bar.paragraph_format.space_after = Pt(2)
run = bar.add_run("DZIEŃ 3 / ŚRODA")
run.font.size = Pt(12); run.font.bold = True; run.font.color.rgb = ACCENT; run.font.name = "Calibri"
add_heading(doc, "KARDIO — Bieg", size=19, color=NAVY, space_after=2)
add_subtitle(doc, "Trening tlenowy dla redukcji tłuszczu i kondycji. Bez rujnowania regeneracji nóg.")
add_table(doc, ["Element", "Wykonanie"], [
    ["Dystans", "8–10 km"],
    ["Tempo / strefa", "Strefa 2 (Z2) — tempo rozmowowe, ~65–75% max HR"],
    ["Rozgrzewka", "5 min marsz / trucht + 4×20 s przyspieszenia"],
    ["Schłodzenie", "5 min spokojny marsz + rozciąganie łydek i bioder"],
    ["Cel", "Wydatek energetyczny + baza tlenowa, NIE interwały"],
], widths=[1.8, 5.7])
add_para(doc, "Jeśli po wtorkowych nogach czujesz się rozbity — skróć do 6–8 km. Bieg Z2 nie konkuruje z regeneracją siłową tak jak sprinty/HIIT.",
         size=9.5, color=GREY, space_after=0)

add_page_break(doc)

# ---------- CZWARTEK ----------
day_page(
    doc,
    "DZIEŃ 4 / CZWARTEK",
    "GÓRA B — Hipertrofia + CLUSTER",
    "Objętość dla wzrostu mięśni + cluster podciąganie jako bodziec siłowy.",
    EX_HEADERS,
    [
        ["1", "PODCIĄGANIE Z OBCIĄŻENIEM — CLUSTER", "3 klastry × 5×1", "~80% 1RM dodatku (+16 kg)", "20–30 s / 3 min"],
        ["2", "Wyciskanie hantli na skosie", "4 × 8–10", "RPE 8", "2 min"],
        ["3", "Wiosłowanie na wyciągu / chest-supported", "4 × 8–12", "RPE 8–9", "2 min"],
        ["4", "Rozpiętki / cable fly", "3 × 12–15", "RPE 9", "90 s"],
        ["5", "Lateral raise (barki boczne)", "4 × 12–15", "RPE 9", "60–90 s"],
        ["6", "Uginanie młotkowe + face pull (superset)", "3 × 12–15", "RPE 8–9", "60–90 s"],
    ],
    EX_WIDTHS,
    cluster_rows={0},
    note="CLUSTER: 1 powt. → zejście → 20–30 s przerwy → 1 powt. → … ×5 = 1 klaster. Razem 3 klastry, między nimi 3 min. Każde powtórzenie pełny zakres.",
)

add_page_break(doc)

# ---------- PIĄTEK ----------
day_page(
    doc,
    "DZIEŃ 5 / PIĄTEK",
    "DÓŁ B — Hipertrofia (hinge-fokus)",
    "Tył łańcucha, pośladki, czworogłowe, łydki, core. Martwy ciąg technicznie (nie na maksa w deficycie).",
    EX_HEADERS,
    [
        ["1", "Martwy ciąg", "3 × 5", "80% / RPE 8", "3 min"],
        ["2", "Hip thrust (pośladki)", "3 × 8–10", "RPE 8–9", "2 min"],
        ["3", "Wykroki / przysiad bułgarski", "3 × 8–10 / noga", "RPE 8", "90–120 s"],
        ["4", "Prostowanie nóg (czworogłowe)", "3 × 12–15", "RPE 9", "90 s"],
        ["5", "Wspięcia na palce (inny kąt)", "4 × 12–15", "RPE 9", "60–90 s"],
        ["6", "Core: hanging leg raise", "3 × 10–12", "RPE 8", "60–90 s"],
    ],
    EX_WIDTHS,
    note="W deficycie martwy ciąg trzymaj technicznie — jakość, nie ego. To ostatni ciężki dzień przed weekendem.",
)

add_page_break(doc)

# ---------- SOBOTA ----------
bar = doc.add_paragraph()
bar.paragraph_format.space_after = Pt(2)
run = bar.add_run("DZIEŃ 6 / SOBOTA")
run.font.size = Pt(12); run.font.bold = True; run.font.color.rgb = ACCENT; run.font.name = "Calibri"
add_heading(doc, "KARDIO LEKKIE — Regeneracja aktywna", size=19, color=NAVY, space_after=2)
add_subtitle(doc, "Spokojny wysiłek wspierający regenerację i dodatkowy wydatek energetyczny.")
add_table(doc, ["Element", "Wykonanie"], [
    ["Opcja A", "Bieg spokojny 5–8 km (wolniej niż w środę)"],
    ["Opcja B", "Marsz / spacer 45–60 min (jeśli zmęczenie)"],
    ["Tempo", "Bardzo lekkie — masz się zregenerować, nie zmęczyć"],
    ["Cel", "Krążenie, redukcja, mobilność — bez obciążania nóg"],
], widths=[1.8, 5.7])
add_para(doc, "Słuchaj ciała: jeśli tydzień był ciężki lub sen słaby, wybierz spacer zamiast biegu.",
         size=9.5, color=GREY, space_after=0)

add_page_break(doc)

# ---------- NIEDZIELA ----------
bar = doc.add_paragraph()
bar.paragraph_format.space_after = Pt(2)
run = bar.add_run("DZIEŃ 7 / NIEDZIELA")
run.font.size = Pt(12); run.font.bold = True; run.font.color.rgb = ACCENT; run.font.name = "Calibri"
add_heading(doc, "ODPOCZYNEK", size=19, color=NAVY, space_after=2)
add_subtitle(doc, "Pełna regeneracja — kluczowa dla wzrostu mięśni i siły, zwłaszcza w deficycie kalorycznym.")
add_table(doc, ["Priorytet", "Zalecenie"], [
    ["Sen", "7–9 godzin — najważniejszy czynnik regeneracji"],
    ["Aktywność", "Brak treningu; ewentualnie lekki spacer"],
    ["Odżywianie", "Trzymaj białko ~160 g nawet w dniu wolnym"],
    ["Regeneracja", "Rozciąganie, rolowanie, nawodnienie"],
], widths=[1.8, 5.7])

add_page_break(doc)

# ---------- CLUSTER — INSTRUKCJA ----------
add_heading(doc, "CLUSTER SETS — instrukcja", size=20, color=ACCENT)
add_subtitle(doc, "Metoda dla rozwoju siły: pojedyncze powtórzenia z krótkimi przerwami wewnątrz serii, przy wysokiej intensywności bez spadku jakości.")

add_heading(doc, "Podciąganie z obciążeniem (stały element)", size=13)
add_bullets(doc, [
    "Obciążenie: ~80% 1RM dodatku. Przy maksie +20 kg na łańcuchu → rób +16 kg.",
    "Wykonanie: 1 powtórzenie → kontrolowane zejście → 20–30 s przerwy → kolejne 1 powtórzenie.",
    "Powtórz do 5 pojedynczych powtórzeń = 1 klaster.",
    "Wykonaj 3 klastry, między klastrami 3 minuty przerwy.",
    "Każde powtórzenie: pełny zakres ruchu, kontrolowany negatyw.",
])

add_heading(doc, "Które ćwiczenia nadają się na cluster", size=13)
add_para(doc, "Cluster najlepiej działa na ćwiczeniach WIELOSTAWOWYCH (dużo mięśni naraz), z łatwym resetem między powtórzeniami. Na izolacjach nie ma sensu.")
add_table(doc, ["Ćwiczenie", "Cluster?", "Dlaczego"], [
    ["Podciąganie z obciążeniem", "TAK — stały element", "Łatwy reset, wysoka intensywność"],
    ["Wyciskanie leżąc", "TAK (opcjonalnie)", "Wielostawowe, łatwy reset na stojakach"],
    ["OHP / żołnierskie", "TAK (opcjonalnie)", "Wielostawowe, cluster utrzymuje jakość"],
    ["Dipy z obciążeniem", "TAK (opcjonalnie)", "Krótki ROM, łatwa pauza"],
    ["Przysiad", "Raczej NIE", "Setup i zmęczenie core > korzyść; lepiej klasyczne serie"],
    ["Martwy ciąg", "NIE", "Każde powt. = pełny setup; lepiej klasyczne single/double"],
    ["Wiosłowanie", "NIE", "Nie max-effort; klasyczne serie wystarczą"],
    ["Izolacje (biceps, łydki, barki boczne)", "NIE", "Za mała korzyść dla siły"],
], widths=[2.3, 1.7, 3.5])

add_para(doc, "W tym planie (redukcja + hipertrofia) cluster stosujemy głównie na podciąganiu. Bench/OHP/dipy możesz dodać jako cluster później, jeśli chcesz mocniej dociągnąć siłę pchania.",
         size=9.5, color=GREY, space_after=0)

add_page_break(doc)

# ---------- PROGRESJA + DIETA ----------
add_heading(doc, "PROGRESJA, REGENERACJA, DIETA", size=20, color=ACCENT)

add_heading(doc, "Kiedy zwiększać ciężar", size=13)
add_table(doc, ["Sytuacja", "Działanie"], [
    ["Wszystkie serie w zakresie powt., RPE ≤ 8", "+2,5 kg (sztanga) lub +1–2 powt. (hantle)"],
    ["RPE 9–10, ledwo domykasz zakres", "Zostań przy tym samym ciężarze"],
    ["Cluster podciąganie 3×5×1 @+16 kg łatwe (RPE ≤8)", "+1–2 kg na łańcuchu"],
    ["2 tygodnie bez postępu", "Sprawdź sen / kalorie / białko; rozważ deload"],
    ["Co 6–8 tygodni", "Deload: −40% objętości, −10% ciężaru, 1 tydzień"],
], widths=[3.6, 3.9])

add_heading(doc, "Zasady w deficycie kalorycznym", size=13)
add_bullets(doc, [
    "Siła może rosnąć wolniej — utrzymanie ciężarów + drobne PR to już sukces.",
    "Trzymaj INTENSYWNOŚĆ (ciężar); jeśli brakuje regeneracji, tnij raczej OBJĘTOŚĆ (serie).",
    "Priorytet: sen 7–9 h, białko 2 g/kg, umiarkowany deficyt.",
])

add_heading(doc, "Dieta — minimum, które musi grać", size=13)
add_table(doc, ["Parametr", "Cel"], [
    ["Białko", "~160 g/dzień (2 g na 1 kg masy ciała)"],
    ["Deficyt", "~300–500 kcal/dzień (nie więcej)"],
    ["Tempo redukcji", "~0,3–0,5 kg/tydzień"],
    ["Nawodnienie", "~30–35 ml/kg masy ciała dziennie"],
], widths=[2.2, 5.3])

add_heading(doc, "Dlaczego ten plan maksymalizuje Twoje cele", size=13)
add_bullets(doc, [
    "MIĘŚNIE: każda partia 2×/tydzień, 12–18 serii/grupę, zakresy 4–15 — pełne spektrum bodźców.",
    "SIŁA: ciężkie 4–6 powt. na bench/przysiad/martwy/OHP + cluster podciąganie.",
    "TŁUSZCZ: 2 biegi + deficyt + wysokie białko.",
    "REGENERACJA: tylko 4 dni siły — w deficycie realnie się zregenerujesz (lepsze niż 6× średnio).",
])

# ---------- STOPKA (numery stron) ----------
def add_page_numbers(doc):
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(qn("w:fldCharType"), "begin")
        instrText = OxmlElement("w:instrText")
        instrText.set(qn("xml:space"), "preserve")
        instrText.text = "PAGE"
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(qn("w:fldCharType"), "end")
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        run.font.size = Pt(9)
        run.font.color.rgb = GREY


add_page_numbers(doc)

doc.save("Plan_treningowy.docx")
print("Zapisano: Plan_treningowy.docx")
