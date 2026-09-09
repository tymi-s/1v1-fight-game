"""Generator arkusza treningowego (Excel .xlsx) na wrzesień i październik 2026.

Plan hipertrofia: pośladki + plecy, redukcja tłuszczu. Dzień po dniu, z pustymi
polami na powtórzenia i ciężar. Arkusz "Progres (rekordy)" ze szacowanym 1RM.
"""

import calendar
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import plan_gf_data as P

# ---------------- Kolory / style ----------------
PLUM = "6C2B5A"        # dni siłowe
GREEN = "117A65"       # kardio
GREY = "7F8C8D"        # odpoczynek
HDR = "4A235A"         # nagłówek kolumn
INPUT_FILL = "FFFDE7"  # pola do wpisania
ZEBRA = "F5F2F7"
GLUTE = "F7E9F2"
WHITE = "FFFFFF"

thin = Side(style="thin", color="D9CCD6")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

F_HDR = Font(name="Calibri", size=11, bold=True, color=WHITE)
F_DAY = Font(name="Calibri", size=12, bold=True, color=WHITE)
F_EX = Font(name="Calibri", size=10, bold=True, color="1A1A1A")
F_CELL = Font(name="Calibri", size=10, color="1A1A1A")
F_TARGET = Font(name="Calibri", size=9, color="555555")

CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

HEADERS = ["Data", "Ćwiczenie", "Seria", "Cel (powt. / RPE / start)",
           "Powt. wykonane", "Ciężar [kg]", "RPE / Notatki"]
COL_W = [16, 36, 8, 30, 14, 12, 24]


def style_month_sheet(ws):
    for i, w in enumerate(COL_W, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c, h in enumerate(HEADERS, start=1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = F_HDR
        cell.fill = PatternFill("solid", fgColor=HDR)
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
    day = P.PLAN[wd]
    wtype = day["type"]
    label = f"{P.WEEKDAYS_PL[wd]}, {date_obj.day} {P.MONTH_GEN[date_obj.month]}"
    color = {"silownia": PLUM, "kardio": GREEN, "odpoczynek": GREY}[wtype]

    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
    hc = ws.cell(row=row, column=1, value=f"{label}  —  {day['title']}")
    hc.font = F_DAY
    hc.fill = PatternFill("solid", fgColor=color)
    hc.alignment = LEFT
    for c in range(1, 8):
        ws.cell(row=row, column=c).border = BORDER
    ws.row_dimensions[row].height = 22
    row += 1

    if wtype == "silownia":
        for name, nsets, reps, inten, rest in day["exercises"]:
            target = f"{reps} / {inten}"
            start = row
            for s in range(1, nsets + 1):
                cs = ws.cell(row=row, column=3, value=s)
                cs.font = F_CELL
                cs.alignment = CENTER
                fill_row_border(ws, row, fill_input=True)
                ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=ZEBRA)
                row += 1
            end = row - 1
            if end > start:
                ws.merge_cells(start_row=start, start_column=2, end_row=end, end_column=2)
                ws.merge_cells(start_row=start, start_column=4, end_row=end, end_column=4)
            bc = ws.cell(row=start, column=2, value=name)
            bc.font = F_EX
            bc.alignment = LEFT
            dc = ws.cell(row=start, column=4, value=target)
            dc.font = F_TARGET
            dc.alignment = CENTER
    elif wtype == "kardio":
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=4)
        ic = ws.cell(row=row, column=2, value=day["info"])
        ic.font = F_TARGET
        ic.alignment = LEFT
        fill_row_border(ws, row, fill_input=True)
        ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=ZEBRA)
        row += 1
    else:  # odpoczynek
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=7)
        rc = ws.cell(row=row, column=2, value=day["info"])
        rc.font = F_CELL
        rc.alignment = LEFT
        for c in range(1, 8):
            ws.cell(row=row, column=c).border = BORDER
        ws.cell(row=row, column=1).fill = PatternFill("solid", fgColor=ZEBRA)
        row += 1

    row += 1  # odstęp
    return row


def build_month(wb, year, month):
    name = {9: "Wrzesień 2026", 10: "Październik 2026"}[month]
    ws = wb.create_sheet(title=name)
    style_month_sheet(ws)
    row = 2
    for d in range(1, calendar.monthrange(year, month)[1] + 1):
        row = add_day_block(ws, row, datetime.date(year, month, d))
    return ws


def build_instrukcja(wb):
    ws = wb.create_sheet(title="Instrukcja", index=0)
    ws.column_dimensions["A"].width = 100
    lines = [
        ("PLAN TRENINGOWY — hipertrofia (pośladki + plecy) i redukcja", True, 14, PLUM),
        ("", False, 11, None),
        ("Cel: zbudować pośladki i plecy, ograniczyć rozbudowę ud, zredukować tłuszcz.", False, 11, None),
        ("", False, 11, None),
        ("Jak korzystać:", True, 12, PLUM),
        ("1. Wybierz zakładkę z miesiącem (Wrzesień 2026 / Październik 2026).", False, 11, None),
        ("2. Nagłówek dnia: śliwkowy = siłownia, zielony = kardio, szary = odpoczynek.", False, 11, None),
        ("3. W dni siłowe wypełniaj żółte pola: powt. wykonane, ciężar [kg], RPE/notatki.", False, 11, None),
        ("4. Kolumna 'Cel' podaje docelowe powtórzenia, RPE i sugerowany ciężar startowy.", False, 11, None),
        ("", False, 11, None),
        ("Ważne — chudnięcie punktowe nie istnieje:", True, 12, "B5347E"),
        ("Tłuszcz z brzucha i dolnych pleców schodzi przy deficycie kalorycznym (z całego ciała).", False, 11, None),
        ("Ćwiczenia core budują mięśnie, ale nie spalają tłuszczu lokalnie — o redukcji decyduje dieta.", False, 11, None),
        ("", False, 11, None),
        ("Pośladki tak, uda (przód) minimalnie:", True, 12, PLUM),
        ("Ruchy biodro-dominujące (hip thrust, RDL, odwodzenie, back extension, kickback) budują pośladek.", False, 11, None),
        ("Świadomie bez prostowania nóg (czwórki) i ciężkiego leg press — one rozbudowują przód uda.", False, 11, None),
        ("Step up i RDL: tułów lekko w przód, nacisk na piętę = akcent na pośladek.", False, 11, None),
        ("", False, 11, None),
        ("Progresja:", True, 12, PLUM),
        ("• Górny zakres powt. przy RPE ≤ 8 → dołóż mały ciężar (+2,5 kg maszyna / +1–2 kg hantle).", False, 11, None),
        ("• Zakres jeszcze niepełny → zostań przy ciężarze i dokładaj powtórzenia.", False, 11, None),
        ("• RPE 9–10 i technika się psuje → utrzymaj lub zmniejsz ciężar.", False, 11, None),
        ("• Co 6–8 tygodni lżejszy tydzień (deload): −30–40% objętości.", False, 11, None),
        ("", False, 11, None),
        ("Dieta:", True, 12, PLUM),
        ("Białko 1,6–2,2 g/kg, umiarkowany deficyt (~300–500 kcal), tempo ~0,3–0,5 kg/tydzień.", False, 11, None),
        ("", False, 11, None),
        ("Zakładka 'Progres (rekordy)': zapisuj najlepsze wyniki; 'Szac. 1RM' liczy się sam (Epley).", False, 11, None),
    ]
    for i, (text, bold, size, color) in enumerate(lines, start=1):
        cell = ws.cell(row=i, column=1, value=text)
        cell.font = Font(name="Calibri", size=size, bold=bold, color=(color if color else "1A1A1A"))
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
        cell.fill = PatternFill("solid", fgColor=HDR)
        cell.alignment = CENTER
        cell.border = BORDER
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 26

    examples = ["Hip thrust", "Odwodzenie na maszynie", "Martwy ciąg rumuński (RDL)",
                "Ściąganie drążka / podciąganie", "Wiosłowanie"]
    for r in range(2, 62):
        for c in range(1, 7):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER
            cell.alignment = LEFT if c in (2, 6) else CENTER
            if c in (1, 2, 3, 4, 6):
                cell.fill = PatternFill("solid", fgColor=INPUT_FILL)
        ws.cell(row=r, column=5).value = (
            f'=IF(AND(C{r}<>"",D{r}<>""),ROUND(C{r}*(1+D{r}/30),1),"")'
        )
        ws.cell(row=r, column=5).font = F_CELL
    for idx, ex in enumerate(examples, start=2):
        c = ws.cell(row=idx, column=2, value=ex)
        c.font = Font(name="Calibri", size=10, italic=True, color="999999")


# ---------------- Budowa ----------------
wb = Workbook()
wb.remove(wb.active)
build_instrukcja(wb)
build_month(wb, 2026, 9)
build_month(wb, 2026, 10)
build_progres(wb)
wb.save("Trening_dziewczyna_wrzesien_pazdziernik_2026.xlsx")
print("Zapisano: Trening_dziewczyna_wrzesien_pazdziernik_2026.xlsx")
