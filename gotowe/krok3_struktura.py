"""Krok 3. Odpowiedź o ustalonym kształcie: agent zamienia opis wydatków w tabelę.

Uruchomienie:  python krok3_struktura.py
"""

from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

load_dotenv()


class Wydatek(BaseModel):
    co: str = Field(description="Na co wydano pieniądze, w dwóch-trzech słowach")
    kwota: float = Field(gt=0, description="Kwota w złotych")
    kategoria: Literal["jedzenie", "transport", "dom", "rozrywka", "inne"]


agent = Agent(
    "openrouter:openai/gpt-5-mini",
    output_type=list[Wydatek],
    instructions="Wypisz wszystkie wydatki, o których pisze użytkownik. Nie dodawaj niczego od siebie.",
)

while True:
    tekst = input("\nOpisz swoje wydatki: ")
    if tekst.strip().lower() in ("", "koniec"):
        break
    wynik = agent.run_sync(tekst)

    # wynik.output to lista obiektów Wydatek, a nie tekst. Liczy już Python, nie model.
    for wydatek in wynik.output:
        print(f"{wydatek.co:<30} {wydatek.kwota:>9.2f} zł   {wydatek.kategoria}")
    print(f"{'RAZEM':<30} {sum(w.kwota for w in wynik.output):>9.2f} zł")
