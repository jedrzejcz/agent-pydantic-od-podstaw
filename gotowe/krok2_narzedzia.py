"""Krok 2. Agent z narzędziami: sprawdza datę i kursy walut NBP.

Uruchomienie:  python krok2_narzedzia.py
"""

import json
from datetime import date
from urllib.request import urlopen

from dotenv import load_dotenv
from pydantic_ai import Agent, ModelRetry

load_dotenv()

agent = Agent(
    "openrouter:openai/gpt-5-mini",
    instructions="""
Jesteś asystentem do spraw walutowych. Odpowiadaj po polsku, krótko.
Kursy walut sprawdzaj zawsze narzędziem kurs_waluty, nigdy nie podawaj ich z pamięci.
""",
)


@agent.tool_plain
def dzisiaj() -> str:
    """Podaje dzisiejszą datę. Użyj, gdy odpowiedź zależy od dzisiejszej daty."""
    return date.today().isoformat()


@agent.tool_plain
def kurs_waluty(kod: str) -> str:
    """Podaje średni kurs waluty w złotych według Narodowego Banku Polskiego.

    Args:
        kod: Trzyliterowy kod waluty, np. EUR, USD, GBP, CHF.
    """
    adres = f"https://api.nbp.pl/api/exchangerates/rates/a/{kod.lower()}/?format=json"
    try:
        with urlopen(adres, timeout=10) as odpowiedz:
            dane = json.load(odpowiedz)
    except OSError as blad:
        # ModelRetry oddaje komunikat agentowi, a agent może spróbować jeszcze raz.
        raise ModelRetry(f"Nie udało się pobrać kursu {kod}: {blad}. Sprawdź kod waluty.")
    kurs = dane["rates"][0]
    return f"1 {dane['code']} = {kurs['mid']} zł (kurs NBP z dnia {kurs['effectiveDate']})"


while True:
    pytanie = input("\nTy: ")
    if pytanie.strip().lower() in ("", "koniec"):
        break
    wynik = agent.run_sync(pytanie)

    # Pokazuje, po które narzędzia agent sięgnął, zanim odpowiedział.
    for wiadomosc in wynik.new_messages():
        for czesc in wiadomosc.parts:
            if czesc.part_kind == "tool-call":
                print(f"  [narzędzie] {czesc.tool_name} {czesc.args}")

    print("Agent:", wynik.output)
