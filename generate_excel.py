"""Generator arkusza treningowego (Excel .xlsx) na wrzesień i październik 2026.

Dzień po dniu wg planu Góra/Dół x2 + kardio. Dla każdego dnia siłowego
rozpisane ćwiczenia i serie z pustymi polami na: powtórzenia wykonane oraz ciężar.
Dodatkowo arkusz "Progres (rekordy)" do śledzenia PR i szacowanego 1RM.
"""

import calendar
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ---------------- Kolory / style ----------------
NAVY = "1F3A5F"        # dni siłowe
GREEN = "117A65"       # kardio
GREY = "7F8C8D"        # odpoczynek
CLUSTER = "C0392B"     # akcent cluster
HDR_GREY = "34495E"    # nagłówek kolumn
INPUT_FILL = "FFFDE7"  # pola do wpisania
ZEBRA = "F2F5F9"

WHITE = "FFFFFF"

thin = Side(style="thin", color="CCCCCC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

F_HDR = Font(name="Calibri", size=11, bold=True, color=WHITE)
F_DAY = Font(name="Calibri", size=12, bold=True, color=WHITE)
F_EX = Font(name="Calibri", size=10, bold=True, color="1A1A1A")
F_CELL = Font(name="Calibri", size=10, color="1A1A1A")
F_TARGET = Font(name="Calibri", size=9, color="555555")
F_CLUSTER = Font(name="Calibri", size=10, bold=True, color=CLUSTER)

CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

# ---------------- Definicja treningów ----------------
# Każde ćwiczenie: (nazwa, liczba_serii, cel, etykieta_serii)
GORA_A = {
    "title": "GÓRA A — Siła (klatka / plecy / barki / ramiona)",
    "type": "silownia",
    "exercises": [
        ("Wyciskanie leżąc (sztanga)", 4, "4–6 @ 80–85% / RPE 8"),
        ("Wiosłowanie sztangą / Pendlay row", 4, "5–6 / RPE 8"),
        ("OHP — wyciskanie żołnierskie", 3, "6–8 / RPE 8"),
        ("Podciąganie z obciążeniem", 3, "5–6 / RPE 8"),
        ("Prostowanie tricepsa (wyciąg)", 3, "8–10 / RPE 8–9"),
        ("Uginanie bicepsa (sztanga/hantle)", 3, "8–10 / RPE 8–9"),
    ],
}
DOL_A = {
    "title": "DÓŁ A — Siła (przysiad-fokus)",
    "type": "silownia",
    "exercises": [
        ("Przysiad ze sztangą", 4, "4–6 @ 80% / RPE 8"),
        ("Martwy ciąg rumuński (RDL)", 3, "6–8 / RPE 8"),
        ("Leg press / hack squat", 3, "8–10 / RPE 8"),
        ("Uginanie nóg leżąc (dwugłowe)", 3, "10–12 / RPE 8–9"),
        ("Wspięcia na palce (łydki)", 4, "10–12 / RPE 9"),
        ("Core: Pallof press / rollout", 3, "8–10 / RPE 8"),
    ],
}
GORA_B = {
    "title": "GÓRA B — Hipertrofia + CLUSTER podciąganie",
    "type": "silownia",
    "exercises": [
        ("Podciąganie z obciążeniem — CLUSTER", 3, "aż do spadku prędkości @ ~80% dodatku", "cluster"),
        ("Wyciskanie hantli na skosie", 4, "8–10 / RPE 8"),
        ("Wiosłowanie na wyciągu / chest-supported", 4, "8–12 / RPE 8–9"),
        ("Rozpiętki / cable fly", 3, "12–15 / RPE 9"),
        ("Lateral raise (barki boczne)", 4, "12–15 / RPE 9"),
        ("Uginanie młotkowe + face pull (superset)", 3, "12–15 / RPE 8–9"),
    ],
}
DOL_B = {
    "title": "DÓŁ B — Hipertrofia (hinge-fokus)",
    "type": "silownia",
    "exercises": [
        ("Martwy ciąg", 3, "5 @ 80% / RPE 8"),
        ("Hip thrust (pośladki)", 3, "8–10 / RPE 8–9"),
        ("Wykroki / przysiad bułgarski", 3, "8–10 / noga / RPE 8"),
        ("Prostowanie nóg (czworogłowe)", 3, "12–15 / RPE 9"),
        ("Wspięcia na palce (inny kąt)", 4, "12–15 / RPE 9"),
        ("Core: hanging leg raise", 3, "10–12 / RPE 8"),
    ],
}
KARDIO_SR = {"title": "KARDIO — Bieg 8–10 km (strefa 2)", "type": "kardio",
             "info": "8–10 km, tempo rozmowowe (Z2). Wpisz: dystans / czas / tempo."}
KARDIO_SB = {"title": "MAŁE KARDIO — 8 km biegu", "type": "kardio",
             "info": "8 km spokojnie (Z2). Wpisz: dystans / czas / tempo."}
ODPOCZYNEK = {"title": "ODPOCZYNEK — regeneracja, sen 7–9 h", "type": "odpoczynek"}

# weekday(): 0=pon ... 6=niedz
PLAN = {0: GORA_A, 1: DOL_A, 2: KARDIO_SR, 3: GORA_B, 4: DOL_B, 5: KARDIO_SB, 6: ODPOCZYNEK}

WEEKDAYS_PL = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
MONTH_GEN = {9: "września", 10: "października"}

HEADERS = ["Data", "Ćwiczenie", "Seria", "Cel (powt./%/RPE)",
           "Powt. wykonane", "Ciężar [kg]", "RPE / Notatki"]
COL_W = [16, 34, 11, 26, 14, 12, 24]


def style_month_sheet(ws):
    for i, w in enumerate(COL_W, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c, h in enumerate(HEADERS, start=1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = F_HDR
        cell.fill = PatternFill("solid", fgColor=HDR_GREY)
        cell.alignment = CENTER
        cell.border = BORDER
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 28


def fill_row_border(ws, row, fill_input=False):
    for c in range(1, 8):
        cell = ws.cell(row=row, column=c)
        cell.border = BORDER
        if fill_input and c in (5, 6, 7):
            cell.fill = PatternFill("solid", fgColor=INPUT_FILL)


def add_day_block(ws, row, date_obj):
    wd = date_obj.weekday()
    workout = PLAN[wd]
    wtype = workout["type"]
    day_label = f"{WEEKDAYS_PL[wd]}, {date_obj.day} {MONTH_GEN[date_obj.month]}"

    # Kolor nagłówka dnia
    color = {"silownia": NAVY, "kardio": GREEN, "odpoczynek": GREY}[wtype]

    # Wiersz nagłówka dnia (scalony A:G)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
    hc = ws.cell(row=row, column=1, value=f"{day_label}  —  {workout['title']}")
    hc.font = F_DAY
    hc.fill = PatternFill("solid", fgColor=color)
    hc.alignment = LEFT
    for c in range(1, 8):
        ws.cell(row=row, column=c).border = BORDER
    ws.row_dimensions[row].height = 22
    row += 1

    if wtype == "silownia":
        for ex in workout["exercises"]:
            name, n_sets, target = ex[0], ex[1], ex[2]
            is_cluster = len(ex) > 3 and ex[3] == "cluster"
            start = row
            for s in range(1, n_sets + 1):
                # C: seria
                seria = f"Klaster {s}" if is_cluster else s
                cser = ws.cell(row=row, column=3, value=seria)
                cser.font = F_CLUSTER if is_cluster else F_CELL
                cser.alignment = CENTER
                fill_row_border(ws, row, fill_input=True)
                # zebra na kolumnie A (pusta) dla czytelności
                ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=ZEBRA)
                row += 1
            end = row - 1
            # B: nazwa ćwiczenia (scalona przez serie)
            if end > start:
                ws.merge_cells(start_row=start, start_column=2, end_row=end, end_column=2)
                ws.merge_cells(start_row=start, start_column=4, end_row=end, end_column=4)
            bc = ws.cell(row=start, column=2, value=name)
            bc.font = F_CLUSTER if is_cluster else F_EX
            bc.alignment = LEFT
            if is_cluster:
                bc.fill = PatternFill("solid", fgColor="FBE9E7")
            dc = ws.cell(row=start, column=4, value=target)
            dc.font = F_TARGET
            dc.alignment = CENTER
    elif wtype == "kardio":
        # jeden wiersz, pola na wpis
        ws.cell(row=row, column=2, value="Bieg").font = F_EX
        ws.cell(row=row, column=2).alignment = LEFT
        ws.cell(row=row, column=3, value="—").alignment = CENTER
        ws.cell(row=row, column=3).font = F_CELL
        dc = ws.cell(row=row, column=4, value=workout["info"])
        dc.font = F_TARGET
        dc.alignment = LEFT
        fill_row_border(ws, row, fill_input=True)
        ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=ZEBRA)
        row += 1
    else:  # odpoczynek
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=7)
        rc = ws.cell(row=row, column=2, value="Odpoczynek — sen 7–9 h, białko ~160 g, ewentualnie spacer")
        rc.font = F_CELL
        rc.alignment = LEFT
        for c in range(1, 8):
            ws.cell(row=row, column=c).border = BORDER
        ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=ZEBRA)
        row += 1

    # pusty wiersz odstępu
    row += 1
    return row


def build_month(wb, year, month):
    name = {9: "Wrzesień 2026", 10: "Październik 2026"}[month]
    ws = wb.create_sheet(title=name)
    style_month_sheet(ws)
    row = 2
    n_days = calendar.monthrange(year, month)[1]
    import datetime
    for d in range(1, n_days + 1):
        row = add_day_block(ws, row, datetime.date(year, month, d))
    return ws


def build_instrukcja(wb):
    ws = wb.create_sheet(title="Instrukcja", index=0)
    ws.column_dimensions["A"].width = 100
    lines = [
        ("PLAN TRENINGOWY — arkusz do śledzenia progresu", True, 14, NAVY),
        ("", False, 11, None),
        ("Jak korzystać:", True, 12, NAVY),
        ("1. Wybierz zakładkę z miesiącem (Wrzesień 2026 / Październik 2026).", False, 11, None),
        ("2. Każdy dzień ma kolorowy nagłówek: granatowy = siłownia, zielony = kardio, szary = odpoczynek.", False, 11, None),
        ("3. W dni siłowe każde ćwiczenie ma rozpisane serie. Wypełniaj żółte pola:", False, 11, None),
        ("     • 'Powt. wykonane' — ile powtórzeń zrobiłeś w danej serii,", False, 11, None),
        ("     • 'Ciężar [kg]' — z jakim obciążeniem,", False, 11, None),
        ("     • 'RPE / Notatki' — jak ciężka była seria (RPE) lub uwagi.", False, 11, None),
        ("4. Kolumna 'Cel' podpowiada docelowe powtórzenia i intensywność (%/RPE).", False, 11, None),
        ("", False, 11, None),
        ("Cluster (podciąganie w czwartki):", True, 12, CLUSTER),
        ("Pojedyncze powtórzenia z przerwą 20–30 s, aż do pierwszego spadku prędkości/techniki = 1 klaster.", False, 11, None),
        ("Łącznie 3 klastry, przerwa 3 min między nimi. Ciężar ~80% dodatku (część dowieszana).", False, 11, None),
        ("W arkusz wpisuj liczbę wykonanych powtórzeń w każdym klastrze i ciężar dodatku.", False, 11, None),
        ("", False, 11, None),
        ("Progresja:", True, 12, NAVY),
        ("• Wszystkie serie w zakresie powt. i RPE ≤ 8  →  następnym razem +2,5 kg (sztanga) lub +1–2 powt.", False, 11, None),
        ("• RPE 9–10, ledwo domykasz zakres  →  zostań przy tym samym ciężarze.", False, 11, None),
        ("• Klastry podciągania idą łatwo  →  +1–2 kg na łańcuchu.", False, 11, None),
        ("• Co 6–8 tygodni tydzień deload: −40% objętości, −10% ciężaru.", False, 11, None),
        ("", False, 11, None),
        ("Zakładka 'Progres (rekordy)':", True, 12, NAVY),
        ("Zapisuj tam najlepsze wyniki głównych bojów. Kolumna 'Szac. 1RM' liczy się sama (wzór Epleya).", False, 11, None),
    ]
    for i, (text, bold, size, color) in enumerate(lines, start=1):
        cell = ws.cell(row=i, column=1, value=text)
        cell.font = Font(name="Calibri", size=size, bold=bold,
                         color=(color if color else "1A1A1A"))
        cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws.sheet_view.showGridLines = False


def build_progres(wb):
    ws = wb.create_sheet(title="Progres (rekordy)")
    headers = ["Data", "Ćwiczenie", "Ciężar [kg]", "Powt.", "Szac. 1RM", "Notatki"]
    widths = [14, 34, 14, 10, 14, 30]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = F_HDR
        cell.fill = PatternFill("solid", fgColor=HDR_GREY)
        cell.alignment = CENTER
        cell.border = BORDER
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 26

    # tytuł podpowiadający boje
    examples = ["Wyciskanie leżąc", "Przysiad ze sztangą", "Martwy ciąg",
                "OHP", "Podciąganie z obciążeniem (dodatek)"]
    for r in range(2, 62):
        for c in range(1, 7):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER
            cell.alignment = CENTER if c != 2 and c != 6 else LEFT
            if c in (1, 2, 3, 4, 6):
                cell.fill = PatternFill("solid", fgColor=INPUT_FILL)
        # wzór Epleya na szacowany 1RM
        ws.cell(row=r, column=5).value = (
            f'=IF(AND(C{r}<>"",D{r}<>""),ROUND(C{r}*(1+D{r}/30),1),"")'
        )
        ws.cell(row=r, column=5).font = F_CELL
    # podpowiedzi w pierwszych wierszach (kolumna B)
    for idx, ex in enumerate(examples, start=2):
        c = ws.cell(row=idx, column=2, value=ex)
        c.font = Font(name="Calibri", size=10, italic=True, color="999999")


# ---------------- Budowa ----------------
wb = Workbook()
wb.remove(wb.active)  # usuń domyślny arkusz

build_instrukcja(wb)
build_month(wb, 2026, 9)
build_month(wb, 2026, 10)
build_progres(wb)

wb.save("Trening_wrzesien_pazdziernik_2026.xlsx")
print("Zapisano: Trening_wrzesien_pazdziernik_2026.xlsx")
