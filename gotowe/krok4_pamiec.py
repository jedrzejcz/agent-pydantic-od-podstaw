"""Krok 4. Pamięć rozmowy: trener słówek, który pamięta wcześniejsze pytania i punkty.

Uruchomienie:  python krok4_pamiec.py
"""

from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()

agent = Agent(
    "openrouter:openai/gpt-5-mini",
    instructions="""
Jesteś trenerem słówek angielskich. Rozmawiasz po polsku.
Podawaj po jednym polskim słowie do przetłumaczenia na angielski.
Po każdej odpowiedzi powiedz, czy była poprawna, podaj aktualny wynik punktowy i następne słowo.
Nie powtarzaj słów, które już padły.
""",
)

# Tu zbieramy całą rozmowę. Na starcie jest pusta.
historia = []

wynik = agent.run_sync("Zaczynamy.", message_history=historia)
historia = wynik.all_messages()
print("Trener:", wynik.output)

while True:
    odpowiedz = input("\nTy: ")
    if odpowiedz.strip().lower() in ("", "koniec"):
        break
    # Wysyłamy nową wiadomość razem z całą dotychczasową rozmową.
    wynik = agent.run_sync(odpowiedz, message_history=historia)
    historia = wynik.all_messages()
    print("Trener:", wynik.output)
