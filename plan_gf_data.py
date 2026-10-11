"""Dane planu treningowego (hipertrofia: pośladki + plecy, redukcja tłuszczu).

Zgodne z arkuszem Trening_dziewczyna_pazdziernik_listopad_2026.xlsx (generate_excel_gf.py).

Ćwiczenie siłowe: (nazwa, liczba_serii, powtórzenia, intensywność, przerwa)
Dzień cardio: lista sekcji (nagłówek, [(element, wykonanie), ...])
"""

DOL_A = {
    "tag": "DZIEŃ 1 / PONIEDZIAŁEK",
    "title": "DÓŁ A — Pośladki (akcent: hip thrust + RDL)",
    "subtitle": "Rozciągnięcie + skrócenie + unilateralne + izolacja + mało pośladka średniego. "
                "Ruchy biodro-dominujące, minimum pracy na przód uda.",
    "type": "silownia",
    "exercises": [
        ("Hip thrust na maszynie (skrócenie)", 4, "8–12", "RPE 8 (start ~110–120 kg)", "2–3 min"),
        ("RDL (rozciągnięcie)", 3, "8–10", "RPE 8 (start ~30–40 kg)", "2 min"),
        ("Przysiad bułgarski (unilateralne)", 3, "8–10 / noga", "RPE 8, tułów w przód", "90 s"),
        ("Ławka rzymska (izolacja)", 3, "12–15", "RPE 8, plecy zaokrąglone", "90 s"),
        ("Abduktor na maszynie, pochylona w przód", 2, "12–15", "RPE 7–8, lekko", "60 s"),
        ("Łydki", 3, "12–15", "RPE 9", "60–90 s"),
    ],
    "note": "Bułgarski i RDL z wychyleniem tułowia do przodu i naciskiem na piętę — pracuje pośladek, nie przód uda. "
            "Pochylenie w przód na abduktorze przenosi pracę na górną część pośladka wielkiego, mniej na pośladek średni.",
}

WOLNE_WT = {
    "tag": "DZIEŃ 2 / WTOREK",
    "title": "WOLNE",
    "subtitle": "Regeneracja po dniu dołu.",
    "type": "odpoczynek",
    "info": "Bez treningu siłowego. Spacer mile widziany. Opcjonalnie: otwarcie bioder (~15 min).",
}

GORA_A = {
    "tag": "DZIEŃ 3 / ŚRODA",
    "title": "GÓRA A — Plecy, klatka, barki, biceps",
    "subtitle": "Priorytet dla pleców (ściąganie + wiosłowanie) i tylnego aktonu barków.",
    "type": "silownia",
    "exercises": [
        ("Ściąganie drążka", 4, "8–12", "RPE 8", "2 min"),
        ("Wiosłowanie", 3, "10–12", "RPE 8", "2 min"),
        ("Wyciskanie na klatkę na maszynie", 3, "10–12", "RPE 8 (start ~30–40 kg)", "90 s"),
        ("Wznosy bokiem z hantlami", 3, "12–15", "RPE 9", "60 s"),
        ("Biceps — superseria lub zwykłe serie", 3, "10–12 każda", "RPE 8–9", "90 s"),
        ("Face pull na lince", 3, "15–20", "RPE 8 (start ~15–20 kg)", "60–90 s"),
    ],
    "note": "Superseria bicepsa = 1 seria: 3 wariacje jedna po drugiej, bez przerwy — hantle, potem 2 wariacje ze sztangą prostą. "
            "W Excelu w 'kg' wpisz np. 6 / 15 / 12.",
}

DOL_B = {
    "tag": "DZIEŃ 4 / CZWARTEK",
    "title": "DÓŁ B — Pośladki (akcent: sumo + glute bridge)",
    "subtitle": "Drugi dzień pośladków — te same 5 funkcji, inne ćwiczenia.",
    "type": "silownia",
    "exercises": [
        ("Przysiad sumo (rozciągnięcie)", 3, "8–10", "RPE 8, szeroko, kolana na zewnątrz", "2 min"),
        ("KAS glute bridge / glute bridge (skrócenie)", 3, "10–12", "RPE 8–9, pauza 1 s u góry", "2 min"),
        ("Step up na lince (unilateralne)", 3, "10–12 / noga", "RPE 8, nacisk na piętę", "90 s"),
        ("Kickback na lince (izolacja)", 3, "12–15 / noga", "RPE 9", "60 s"),
        ("Rotacja zewn. biodra na lince / gumie", 2, "12 / stronę", "wolno, lekko", "60 s"),
        ("Łydki", 3, "12–15", "RPE 9", "60–90 s"),
    ],
    "note": "Pośladek średni/mały celowo mało i lekko (2 serie) — bez rozbudowy boków pośladków.",
}

CARDIO_PT = {
    "tag": "DZIEŃ 5 / PIĄTEK",
    "title": "CARDIO + BRZUCH + OTWARCIE BIODER",
    "subtitle": "Wsparcie redukcji, wzmocnienie brzucha (mięśnie, nie punktowe spalanie) i mobilność bioder.",
    "type": "kardio",
    "sections": [
        ("Bieg", [
            ("Bieg 5 km", "Tempo rozmowowe (strefa 2). Zamiennie: rower / orbitrek 30–40 min."),
        ]),
        ("Brzuch", [
            ("Plank", "3 × 30–45 s"),
            ("Dead bug", "3 × 10 / stronę"),
            ("Unoszenie kolan w zwisie / spięcia na wyciągu", "3 × 12–15, RPE 8"),
        ]),
        ("Otwarcie bioder (~15 min)", [
            ("Kontrola: hip CARs", "2 × 5 powolnych krążeń / stronę"),
            ("Rotacja wewn.: 90/90 lift-off", "2 × 8 / stronę"),
            ("Rotacja zewn.: gołąb / figure-4", "2 × 30–45 s / stronę"),
            ("Zgięcie: głęboki przysiad (trzymanie)", "2 × 30–45 s"),
            ("Bocznie: przysiad kozacki / żaba", "2 × 6–8 / stronę"),
        ]),
    ],
    "note": "Otwarcie bioder spokojnie i bez bólu. Można je też zrobić jako osobną sesję (wtorek / niedziela).",
}

GORA_B = {
    "tag": "DZIEŃ 6 / SOBOTA",
    "title": "GÓRA B — Plecy, barki, triceps",
    "subtitle": "Drugi dzień góry: pion (podciąganie) + barki + ramiona.",
    "type": "silownia",
    "exercises": [
        ("Podciąganie (guma / maszyna / sama)", 3, "6–10", "RPE 8 (maszyna assist ~12 kg)", "2 min"),
        ("Wyciskanie barków (maszyna / hantle)", 3, "10–12", "RPE 8 (start ~12–20 kg)", "2 min"),
        ("Wiosłowanie", 3, "10–12", "RPE 8", "90 s"),
        ("Triceps na lince", 3, "12–15", "RPE 8–9 (start ~10–12 kg)", "60–90 s"),
        ("Wznosy bokiem z hantlami", 3, "12–15", "RPE 9", "60 s"),
        ("Face pull na lince", 3, "15–20", "RPE 8", "60 s"),
    ],
    "note": "W Excelu przy podciąganiu wpisz wariant (guma / maszyna / sama), przy barkach sprzęt (maszyna / hantle).",
}

ODPOCZYNEK = {
    "tag": "DZIEŃ 7 / NIEDZIELA",
    "title": "ODPOCZYNEK",
    "subtitle": "Pełna regeneracja — mięśnie rosną w czasie odpoczynku.",
    "type": "odpoczynek",
    "info": "Sen 7–9 h, dużo białka, ewentualnie spacer. Bez treningu siłowego.",
}

DAYS_ORDER = [DOL_A, WOLNE_WT, GORA_A, DOL_B, CARDIO_PT, GORA_B, ODPOCZYNEK]

WEEK_OVERVIEW = [
    ("Poniedziałek", "Dół A — Pośladki", "Hip thrust, RDL, bułgarski, ławka rzymska"),
    ("Wtorek", "Wolne", "Regeneracja"),
    ("Środa", "Góra A — Plecy, klatka, barki, biceps", "Ściąganie, wiosłowanie, superseria bicepsa"),
    ("Czwartek", "Dół B — Pośladki", "Sumo, glute bridge, step up, kickback"),
    ("Piątek", "Cardio + brzuch + otwarcie bioder", "Bieg 5 km Z2, core, mobilność"),
    ("Sobota", "Góra B — Plecy, barki, triceps", "Podciąganie, barki, triceps"),
    ("Niedziela", "Odpoczynek", "Regeneracja, sen 7–9 h"),
]

LOWER_STRUCTURE = [
    ("Rozciągnięcie", "RDL", "Przysiad sumo"),
    ("Skrócenie", "Hip thrust na maszynie", "KAS glute bridge"),
    ("Unilateralne", "Przysiad bułgarski", "Step up na lince"),
    ("Izolacja", "Ławka rzymska", "Kickback na lince"),
    ("Pośl. średni / mały (mało)", "Abduktor, pochylona w przód", "Rotacja zewnętrzna"),
]

CELE = [
    ("Redukcja tłuszczu", "Deficyt kaloryczny + kardio + wysokie białko (chudnięcie z CAŁEGO ciała)"),
    ("Pośladki", "2× w tygodniu, każdy dzień: rozciągnięcie, skrócenie, unilateralne, izolacja"),
    ("Kształt pośladków", "Mało pracy na pośladek średni — bez poszerzania boków"),
    ("Plecy", "2× w tygodniu: ściąganie, podciąganie, wiosłowanie, face pull"),
    ("Mobilność bioder", "Rotacja wewn./zewn., zgięcie, bocznie, kontrola — w dzień cardio"),
    ("Białko", "1,6–2,2 g na 1 kg masy ciała dziennie"),
    ("Deficyt", "Umiarkowany, tempo ~0,3–0,5 kg/tydzień"),
]
