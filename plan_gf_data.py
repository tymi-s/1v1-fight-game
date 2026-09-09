"""Dane planu treningowego (hipertrofia: pośladki + plecy, redukcja tłuszczu).

Współdzielone przez generator PDF i Excel, aby oba pliki były spójne.

Każde ćwiczenie: (nazwa, liczba_serii, powtórzenia, intensywność, przerwa)
"""

# Kolejność dni (poniedziałek = 0 ... niedziela = 6)
WEEKDAYS_PL = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
MONTH_GEN = {9: "września", 10: "października"}

DOL_A = {
    "tag": "DZIEŃ 1 / PONIEDZIAŁEK",
    "title": "DÓŁ A — Pośladki (glute-focus)",
    "subtitle": "Akcent na pośladki i tył nóg. Minimum pracy na czworogłowe (uda) — ruchy biodro-dominujące.",
    "type": "silownia",
    "exercises": [
        ("Hip thrust na maszynie", 4, "8–12", "RPE 8 (start ~110–120 kg)", "2–3 min"),
        ("Martwy ciąg rumuński (RDL)", 3, "10–12", "RPE 8 (start ~30–40 kg)", "2 min"),
        ("Odwodzenie na maszynie", 3, "12–15", "RPE 8–9 (start ~70–90 kg)", "90 s"),
        ("Step up na lince", 3, "10–12 / noga", "RPE 8, akcent pośladek", "90 s"),
        ("Cable kickback / pull-through", 3, "12–15", "RPE 8–9 (start ~15–25 kg)", "60–90 s"),
        ("Łydki (wspięcia)", 3, "12–15", "RPE 9 (start ~40–50 kg)", "60–90 s"),
    ],
    "note": "Step up i RDL rób z wychyleniem tułowia do przodu i naciskiem na piętę — wtedy pracuje pośladek, nie przód uda.",
}

GORA_A = {
    "tag": "DZIEŃ 2 / WTOREK",
    "title": "GÓRA A — Plecy + biceps (pull)",
    "subtitle": "Priorytet dla pleców: różne kąty ciągnięcia + tylny akton barków i biceps.",
    "type": "silownia",
    "exercises": [
        ("Ściąganie drążka / podciąganie asystowane", 4, "8–12", "RPE 8 (assist ~12 kg / guma)", "2 min"),
        ("Wiosłowanie hantlami / maszyna", 4, "10–12", "RPE 8 (start ~20–25 kg)", "2 min"),
        ("Wiosłowanie na wyciągu (seated row)", 3, "10–12", "RPE 8 (start ~30–40 kg)", "90 s"),
        ("Face pull na lince", 3, "15–20", "RPE 8 (start ~15–20 kg)", "60–90 s"),
        ("Uginanie bicepsa hantlami", 3, "10–12", "RPE 8–9 (start ~7–10 kg)", "60–90 s"),
        ("Wznosy bokiem (barki)", 3, "12–15", "RPE 8–9 (start ~5–8 kg)", "60 s"),
    ],
}

KARDIO_SR = {
    "tag": "DZIEŃ 3 / ŚRODA",
    "title": "CARDIO + CORE",
    "subtitle": "Wsparcie redukcji tłuszczu i wzmocnienie brzucha (mięśnie, nie punktowe spalanie).",
    "type": "kardio",
    "info": "Bieg 5 km w strefie 2 (tempo rozmowowe) LUB rower/orbitrek 30–40 min.  +  CORE: plank 3×30–45 s, "
            "dead bug 3×10/stronę, spięcia na wyciągu (cable crunch) 3×12–15.",
}

DOL_B = {
    "tag": "DZIEŃ 4 / CZWARTEK",
    "title": "DÓŁ B — Pośladki + tył uda",
    "subtitle": "Drugi dzień pośladków (wysoka częstotliwość = szybszy wzrost) + dwugłowe uda, wciąż bez akcentu na przód uda.",
    "type": "silownia",
    "exercises": [
        ("Hip thrust na maszynie", 3, "10–12", "RPE 8 (lżej niż w pon.)", "2–3 min"),
        ("Uginanie nóg leżąc/siedząc (dwójki)", 3, "10–12", "RPE 8–9 (start ~20–25 kg)", "90 s"),
        ("Ława rzymska / back extension", 3, "12–15", "RPE 8, akcent pośladki (start ~20–30 kg)", "90 s"),
        ("Odwodzenie na maszynie", 3, "15–20", "RPE 9 (start ~60–80 kg)", "60–90 s"),
        ("Step up na lince", 3, "10–12 / noga", "RPE 8, akcent pośladek", "90 s"),
        ("Core: plank / dead bug", 3, "30–45 s / 10", "RPE 8", "60 s"),
    ],
}

KARDIO_PT = {
    "tag": "DZIEŃ 5 / PIĄTEK",
    "title": "CARDIO opcjonalne / odpoczynek",
    "subtitle": "Dodatkowy wydatek energetyczny pod redukcję — albo pełny odpoczynek, jeśli zmęczenie.",
    "type": "kardio",
    "info": "Opcjonalnie: spacer 45–60 min / rower Z2 30–40 min / lekkie interwały 15–20 min. "
            "Jeśli tydzień był ciężki lub sen słaby — pełny odpoczynek.",
}

GORA_B = {
    "tag": "DZIEŃ 6 / SOBOTA",
    "title": "GÓRA B — Klatka, barki, ramiona",
    "subtitle": "Dopełnienie góry (push) + dodatkowa objętość na plecy i ulubione izolacje ramion.",
    "type": "silownia",
    "exercises": [
        ("Wyciskanie na klatkę (maszyna/hantle)", 3, "10–12", "RPE 8 (start ~30–40 kg)", "2 min"),
        ("Wyciskanie barków (hantle/maszyna)", 3, "10–12", "RPE 8 (start ~12–20 kg)", "2 min"),
        ("Ściąganie / wiosłowanie (plecy)", 3, "10–12", "RPE 8", "90 s"),
        ("Triceps na lince", 3, "12–15", "RPE 8–9 (start ~10–12 kg)", "60–90 s"),
        ("Uginanie bicepsa hantlami", 3, "12–15", "RPE 8–9 (start ~7–10 kg)", "60–90 s"),
        ("Face pull na lince", 3, "15–20", "RPE 8 (start ~15–20 kg)", "60 s"),
    ],
}

ODPOCZYNEK = {
    "tag": "DZIEŃ 7 / NIEDZIELA",
    "title": "ODPOCZYNEK",
    "subtitle": "Pełna regeneracja — mięśnie rosną w czasie odpoczynku.",
    "type": "odpoczynek",
    "info": "Sen 7–9 h, dużo białka, ewentualnie spacer. Bez treningu siłowego.",
}

# Mapowanie: weekday() -> dzień
PLAN = {0: DOL_A, 1: GORA_A, 2: KARDIO_SR, 3: DOL_B, 4: KARDIO_PT, 5: GORA_B, 6: ODPOCZYNEK}

# Kolejność dni do PDF
DAYS_ORDER = [DOL_A, GORA_A, KARDIO_SR, DOL_B, KARDIO_PT, GORA_B, ODPOCZYNEK]

# Tabela układu tygodnia (dzień, trening, cel)
WEEK_OVERVIEW = [
    ("Poniedziałek", "Dół A — Pośladki", "Hip thrust, RDL, odwodzenie, step up"),
    ("Wtorek", "Góra A — Plecy + biceps", "Ściąganie, wiosłowania, face pull"),
    ("Środa", "Cardio + core", "Bieg 5 km Z2 + brzuch"),
    ("Czwartek", "Dół B — Pośladki + tył uda", "Hip thrust, dwójki, back extension"),
    ("Piątek", "Cardio opcjonalne / odpoczynek", "Spacer / rower — pod redukcję"),
    ("Sobota", "Góra B — Klatka, barki, ramiona", "Wyciskania + biceps/triceps"),
    ("Niedziela", "Odpoczynek", "Regeneracja, sen 7–9 h"),
]

CELE = [
    ("Redukcja tłuszczu", "Deficyt kaloryczny + kardio + wysokie białko (chudnięcie z CAŁEGO ciała)"),
    ("Pośladki", "2× w tygodniu: hip thrust, odwodzenie, RDL, back extension, kickback"),
    ("Plecy", "2–3× ciągnięcie: ściąganie, wiosłowania, face pull"),
    ("Minimalne uda (czworogłowe)", "Ruchy biodro-dominujące; bez prostowania nóg i ciężkiego leg press"),
    ("Białko", "1,6–2,2 g na 1 kg masy ciała dziennie"),
    ("Deficyt", "Umiarkowany, tempo ~0,3–0,5 kg/tydzień"),
]
