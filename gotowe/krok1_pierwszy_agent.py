"""Krok 1. Pierwszy agent: pytasz w terminalu, agent odpowiada.

Uruchomienie:  python krok1_pierwszy_agent.py
Zakończenie:   wpisz "koniec" albo wciśnij Enter bez tekstu.
"""

from dotenv import load_dotenv
from pydantic_ai import Agent

# Wczytuje klucz OPENROUTER_API_KEY z pliku .env.
load_dotenv()

agent = Agent(
    "openrouter:openai/gpt-5-mini",
    instructions="Jesteś pomocnym asystentem. Odpowiadaj po polsku, krótko i konkretnie.",
)

while True:
    pytanie = input("\nTy: ")
    if pytanie.strip().lower() in ("", "koniec"):
        break
    wynik = agent.run_sync(pytanie)
    print("Agent:", wynik.output)
