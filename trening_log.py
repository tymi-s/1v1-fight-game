"""Wyniki już wpisane w poprzedniej wersji arkusza (przepisane ze zrzutów ekranu).

Klucz: (kod_treningu, data). Wartość: {nazwa_ćwiczenia: [(powt, kg), ...]} oraz
opcjonalnie "_notatka". Wartości jako tekst — tak jak wpisuje się je w arkuszu.
"""

import datetime as _dt

D = _dt.date

LOG = {
    ("GB", D(2026, 9, 3)): {
        "Podciąganie z obciążeniem — CLUSTER": [("6-7", "16")],
        "Wyciskanie hantli na skosie": [("10", "15"), ("8", "17.5"), ("8", "20"), ("8", "20")],
        "Wiosłowanie na wyciągu / chest-supported": [("10", "54"), ("10", "54"), ("8", "54"), ("8", "54")],
        "Lateral raise (barki boczne)": [("10", "8.5"), ("10", "8.5"), ("10", "8.5"), ("10", "8.5")],
        "Uginanie młotkowe + face pull (superset)": [("10", "15 - 34"), ("10", "15 - 34"), ("10", "15 - 34")],
    },
    ("GA", D(2026, 9, 7)): {
        "Wyciskanie leżąc (sztanga)": [("5", "55"), ("5", "60"), ("5", "65"), ("5", "72.5")],
        "Wiosłowanie sztangą / Pendlay row": [("6", "40"), ("6", "50"), ("6", "55"), ("6", "59")],
        "OHP — wyciskanie żołnierskie": [("6", "30"), ("6", "32.5"), ("6", "35")],
        "Podciąganie z obciążeniem": [("5", "5"), ("5", "5"), ("5", "7.5")],
        "Prostowanie tricepsa (wyciąg)": [("8", "27"), ("10", "27"), ("10", "30")],
        "Uginanie bicepsa (sztanga/hantle)": [("8", "15"), ("8", "15"), ("8", "15")],
    },
    ("DA", D(2026, 9, 8)): {
        "Przysiad ze sztangą": [("6", "50"), ("6", "60"), ("6", "65"), ("6", "70")],
        "Martwy ciąg rumuński (RDL)": [("10", "40"), ("6", "55"), ("6", "60")],
        "Leg press / hack squat": [("6", "40"), ("8", "30"), ("8", "30")],
        "Uginanie nóg leżąc (dwugłowe)": [("10", "15"), ("10", "15"), ("10", "17.5")],
        "Wspięcia na palce (łydki)": [("12", "60"), ("12", "60"), ("12", "60"), ("12", "60")],
        "Core: Pallof press / rollout": [("10", "0"), ("10", "0"), ("0", "0")],
    },
    ("GA", D(2026, 9, 14)): {
        "Wyciskanie leżąc (sztanga)": [("5", "50"), ("5", "60"), ("5", "65"), ("5", "70")],
        "Wiosłowanie sztangą / Pendlay row": [("5", "60"), ("5", "65"), ("5", "70")],
        "OHP — wyciskanie żołnierskie": [("8", "33"), ("7", "35"), ("8", "35")],
        "Podciąganie z obciążeniem": [("6", "5"), ("5", "7.5"), ("5", "7.5")],
        "Prostowanie tricepsa (wyciąg)": [("10", "28.75"), ("8", "30"), ("8", "30")],
        "Uginanie bicepsa (sztanga/hantle)": [("8", "12.5"), ("8", "12.5"), ("8", "12.5")],
    },
    ("DA", D(2026, 9, 15)): {
        "Przysiad ze sztangą": [("5", "60"), ("5", "65"), ("5", "70"), ("5", "75")],
        "Martwy ciąg rumuński (RDL)": [("8", "50"), ("8", "55"), ("8", "60")],
        "Leg press / hack squat": [("8", "20"), ("8", "20"), ("8", "20")],
        "Uginanie nóg leżąc (dwugłowe)": [("8", "15"), ("10", "15"), ("10", "17.5")],
        "Wspięcia na palce (łydki)": [("12", "60"), ("12", "60"), ("12", "65"), ("0", "0")],
        "Core: Pallof press / rollout": [("10", ""), ("10", ""), ("10", "")],
    },
    ("DB", D(2026, 10, 9)): {
        "Martwy ciąg": [("5", "57.5"), ("5", "65"), ("5", "70")],
        "Hip thrust (pośladki)": [("10", "40"), ("10", "50"), ("10", "60")],
        "Wykroki / przysiad bułgarski": [("10", "12.5"), ("8", "12.5"), ("8", "12.5")],
        "Prostowanie nóg (czworogłowe)": [("12", "5"), ("12", "7.5"), ("15", "10")],
        "Wspięcia na palce (inny kąt)": [("15", "60"), ("12", "70"), ("12", "75"), ("12", "80")],
        "Core: hanging leg raise": [("12", "0"), ("12", "0"), ("12", "0")],
        "_notatka": "Martwy, seria 2: 5 na 75",
    },
}
