"""Krok 5. Czat w przeglądarce: mistrz gry, który rzuca prawdziwą kostką.

Uruchomienie:  python krok5_czat.py
Czat otworzy się pod adresem http://127.0.0.1:7932
"""

import random

import uvicorn
from dotenv import load_dotenv
from pydantic import Field
from pydantic_ai import Agent

load_dotenv()

agent = Agent(
    "openrouter:openai/gpt-5-mini",
    instructions="""
Jesteś mistrzem gry w krótkiej przygodzie fantasy. Piszesz po polsku, barwnie, ale zwięźle.
Na końcu każdej odpowiedzi daj graczowi dwie albo trzy możliwości do wyboru.
Gdy wynik działania gracza jest niepewny, rzuć kostką narzędziem rzut_kostka
i opisz skutek zależnie od wyniku. Nigdy nie wymyślaj wyniku rzutu sam.
""",
)


@agent.tool_plain
def rzut_kostka(scianki: int = Field(default=20, ge=2, le=100)) -> int:
    """Rzuca kostką i zwraca wynik od 1 do liczby ścianek.

    Args:
        scianki: Liczba ścianek kostki, od 2 do 100, np. 6 albo 20.
    """
    return random.randint(1, scianki)


# Gotowy czat w przeglądarce. Sam pamięta rozmowę, więc nie potrzebujesz listy historia.
app = agent.to_web()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7932)
