# Własny agent w Pydantic AI od podstaw

Na warsztacie dostałeś gotowego asystenta i go zmieniałeś. Tutaj zbudujesz agenta sam, zaczynając od pustego pliku. Przejdziesz pięć kroków. Każdy dodaje jedną nową umiejętność i ma własny, mały przykład.

| Krok | Czego się nauczysz | Przykład |
|---|---|---|
| 1. Pierwszy agent | jak utworzyć agenta, dać mu instrukcję i zadać pytanie | asystent w terminalu |
| 2. Narzędzia | jak dać agentowi funkcje, z których sam korzysta | kursy walut z NBP |
| 3. Odpowiedź o ustalonym kształcie | jak dostać od agenta dane zamiast tekstu | wydatki zamienione w tabelę |
| 4. Pamięć rozmowy | jak sprawić, żeby agent pamiętał, o czym rozmawialiście | trener słówek angielskich |
| 5. Czat w przeglądarce | jak zamienić agenta w okno czatu | mistrz gry, który rzuca kostką |

**Potrzebujesz:**

- komputera z Pythonem 3.11 lub nowszym,
- **własnego klucza API do OpenRoutera**. Jak go zdobyć, opisuje plik [KLUCZ-API.md](KLUCZ-API.md),
- edytora kodu. Polecam [Visual Studio Code](https://code.visualstudio.com/): koloruje kod i pilnuje wcięć.

**Ile to kosztuje?** Wszystkie przykłady korzystają z modelu `openai/gpt-5-mini`. Jedno pytanie kosztuje zwykle ułamek centa, a całą instrukcję przejdziesz za mniej niż dolara. Swoje wydatki sprawdzisz na [openrouter.ai/activity](https://openrouter.ai/activity).

**Jak pracować z tą instrukcją:**

- Każdy krok to nowy plik, który tworzysz w głównym folderze repozytorium.
- Kod z instrukcji możesz skopiować, ale lepiej go przepisać: przepisując, zauważasz szczegóły.
- W folderze `gotowe/` jest działająca wersja każdego kroku. Zajrzyj tam, gdy utkniesz albo coś nie działa.
- W Pythonie **wcięcia mają znaczenie**. Linie wewnątrz `while`, `if`, `for` i funkcji muszą być wcięte czterema spacjami.

## Krok 0. Przygotowanie

Jeśli zostało Ci środowisko z warsztatu, i tak zrób te kroki w nowym folderze. Każdy projekt ma własne środowisko.

### 0.1. Pobierz repozytorium

Na stronie repozytorium kliknij zielony przycisk **Code**, wybierz **Download ZIP** i rozpakuj archiwum, np. na pulpit.

### 0.2. Otwórz terminal w folderze

- **macOS:** w Terminalu wpisz `cd ` (ze spacją na końcu), przeciągnij rozpakowany folder z Findera do okna terminala i wciśnij Enter.
- **Windows:** otwórz rozpakowany folder w Eksploratorze, kliknij pasek adresu, wpisz `powershell` i wciśnij Enter.

Wpisz `ls`. Na liście powinny być `README.md`, `requirements.txt` i folder `gotowe`.

### 0.3. Utwórz środowisko i zainstaluj biblioteki

**macOS i Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Na początku wiersza w terminalu powinno pojawić się `(.venv)`.

*Środowisko (`.venv`) to osobna szuflada na biblioteki tego projektu. Dzięki niej biblioteki z jednego projektu nie mieszają się z innymi.*

### 0.4. Wpisz swój klucz

**macOS:**

```bash
cp .env.example .env
open -e .env
```

**Windows:**

```powershell
copy .env.example .env
notepad .env
```

Zastąp `wklej-tutaj-klucz` swoim kluczem z OpenRoutera (bez spacji i cudzysłowów). Zapisz plik.

### 0.5. Otwórz folder w edytorze

W Visual Studio Code wybierz **File → Open Folder** i wskaż folder z repozytorium. Pliki z kolejnych kroków będziesz tworzyć przez **File → New File**, zapisując je w tym folderze.

*Terminal zostaw otwarty obok. W nim będziesz uruchamiać kolejne pliki.*

## Krok 1. Pierwszy agent

### 1.1. Jedno pytanie, jedna odpowiedź

Utwórz plik `krok1_pierwszy_agent.py` i wpisz:

```python
from dotenv import load_dotenv
from pydantic_ai import Agent

load_dotenv()

agent = Agent(
    "openrouter:openai/gpt-5-mini",
    instructions="Jesteś pomocnym asystentem. Odpowiadaj po polsku, krótko i konkretnie.",
)

wynik = agent.run_sync("Wyjaśnij w dwóch zdaniach, czym jest agent AI.")
print(wynik.output)
```

Zapisz plik i uruchom go w terminalu:

```bash
python krok1_pierwszy_agent.py
```

Po kilku sekundach zobaczysz odpowiedź.

**Co tu się dzieje:**

| Linia | Co robi |
|---|---|
| `from ... import ...` | wczytuje potrzebne biblioteki |
| `load_dotenv()` | odczytuje klucz z pliku `.env` |
| `Agent(...)` | tworzy agenta: podajesz model i instrukcję |
| `"openrouter:openai/gpt-5-mini"` | model: `openrouter:` mówi, przez kogo się łączymy, dalej jest nazwa modelu |
| `instructions=` | instrukcja, czyli kim agent jest i jak ma odpowiadać. Model dostaje ją przy każdym pytaniu |
| `agent.run_sync(...)` | wysyła pytanie i czeka na odpowiedź |
| `wynik.output` | treść odpowiedzi |

### 1.2. Rozmowa w pętli

Zamiast jednego pytania wpisanego w kod niech agent odpowiada na to, co wpiszesz. Zastąp dwie ostatnie linie pliku tym kodem:

```python
while True:
    pytanie = input("\nTy: ")
    if pytanie.strip().lower() in ("", "koniec"):
        break
    wynik = agent.run_sync(pytanie)
    print("Agent:", wynik.output)
```

- `while True:` powtarza wszystko, co jest pod nim wcięte, w nieskończoność.
- `input(...)` czeka, aż coś wpiszesz i wciśniesz Enter.
- `break` przerywa pętlę, gdy wpiszesz `koniec` albo wciśniesz sam Enter.

Uruchom plik jeszcze raz i porozmawiaj z agentem.

### 1.3. Sprawdź, czego agent nie umie

Napisz po kolei:

> Mam na imię Ola.

> Jak mam na imię?

Agent nie wie. Każde `run_sync` to dla niego zupełnie nowa rozmowa. Naprawisz to w kroku 4.

**Ćwiczenie:** zmień instrukcję, np. na „Odpowiadaj jak pirat” albo „Odpowiadaj tylko po angielsku”. Zapisz plik, uruchom go ponownie i zobacz, jak zmienia się styl odpowiedzi.

*Gotowe rozwiązanie: [gotowe/krok1_pierwszy_agent.py](gotowe/krok1_pierwszy_agent.py)*

## Krok 2. Narzędzia

Model sam z siebie nie zna dzisiejszej daty ani dzisiejszych kursów walut. Zapytany, zgaduje. Narzędzie to zwykła funkcja w Pythonie, którą agent może wywołać, gdy potrzebuje prawdziwych danych.

### 2.1. Agent walutowy

Utwórz plik `krok2_narzedzia.py`:

```python
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
        raise ModelRetry(f"Nie udało się pobrać kursu {kod}: {blad}. Sprawdź kod waluty.")
    kurs = dane["rates"][0]
    return f"1 {dane['code']} = {kurs['mid']} zł (kurs NBP z dnia {kurs['effectiveDate']})"


while True:
    pytanie = input("\nTy: ")
    if pytanie.strip().lower() in ("", "koniec"):
        break
    wynik = agent.run_sync(pytanie)

    for wiadomosc in wynik.new_messages():
        for czesc in wiadomosc.parts:
            if czesc.part_kind == "tool-call":
                print(f"  [narzędzie] {czesc.tool_name} {czesc.args}")

    print("Agent:", wynik.output)
```

**Co tu się dzieje:**

- **`@agent.tool_plain`** nad funkcją zgłasza ją agentowi jako narzędzie.
- **Opis w potrójnym cudzysłowie** (docstring) to instrukcja dla agenta: czytając go, agent decyduje, kiedy użyć narzędzia. Pisz go tak, jakbyś tłumaczył zadanie nowej osobie w pracy.
- **`kod: str`** mówi, że narzędzie przyjmuje tekst. Sekcja `Args:` w opisie wyjaśnia agentowi, co ma tam wpisać.
- **`ModelRetry`** oddaje agentowi komunikat o błędzie. Agent może poprawić argument i spróbować jeszcze raz, zamiast przerywać rozmowę.
- **Pętla po `wynik.new_messages()`** wypisuje, po które narzędzia agent sięgnął. Dzięki temu widzisz, czy odpowiedź wzięła się z narzędzia, czy z pamięci modelu.

### 2.2. Przetestuj

| Pytanie | Czego się spodziewać |
|---|---|
| Ile dziś kosztuje euro? | wywołanie `kurs_waluty` z `EUR` |
| Ile złotych dostanę za 250 dolarów? | `kurs_waluty` z `USD` i przeliczenie |
| Co jest droższe: funt czy frank szwajcarski? | dwa wywołania narzędzia |
| Jaki jest kurs waluty XYZ? | błąd z NBP i informacja, że takiej waluty nie ma |
| Jaki dziś dzień tygodnia? | wywołanie `dzisiaj` |

*Kurs z NBP może być z poprzedniego dnia roboczego: bank nie publikuje kursów w weekendy i święta.*

**Ćwiczenie:** dopisz narzędzie `kurs_z_dnia(kod: str, dzien: date)`, które podaje kurs z wybranego dnia. Adres w NBP wygląda tak: `https://api.nbp.pl/api/exchangerates/rates/a/usd/2026-10-01/?format=json`. W miejsce daty wstaw `{dzien}`. Zapytaj potem: „Ile kosztował dolar 1 października 2026?”. Dla soboty NBP zwróci błąd. Sprawdź, czy agent sam spróbuje z innym dniem.

*Gotowe rozwiązanie (bez ćwiczenia): [gotowe/krok2_narzedzia.py](gotowe/krok2_narzedzia.py)*

## Krok 3. Odpowiedź o ustalonym kształcie

Do tej pory agent odpowiadał tekstem. Tekst dobrze się czyta, ale trudno go dalej przetwarzać w programie. Tutaj agent zwróci dane: listę wydatków, z których każdy ma nazwę, kwotę i kategorię.

### 3.1. Agent od wydatków

Utwórz plik `krok3_struktura.py`:

```python
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

    for wydatek in wynik.output:
        print(f"{wydatek.co:<30} {wydatek.kwota:>9.2f} zł   {wydatek.kategoria}")
    print(f"{'RAZEM':<30} {sum(w.kwota for w in wynik.output):>9.2f} zł")
```

**Co tu się dzieje:**

- **`class Wydatek(BaseModel)`** to model Pydantic, czyli opis kształtu danych: jakie pola i jakich typów.
- **`Field(description=...)`** podpowiada agentowi, co wpisać w pole. `gt=0` wymaga kwoty większej od zera.
- **`Literal[...]`** pozwala tylko na wymienione wartości. Agent nie wymyśli własnej kategorii.
- **`output_type=list[Wydatek]`** mówi agentowi, że ma oddać listę wydatków, a nie tekst.
- **`wynik.output`** to teraz lista obiektów. Do pól dostajesz się przez kropkę: `wydatek.kwota`.
- **Sumę liczy Python, nie model.** Modele językowe mylą się w rachunkach, Python nie.

*Jeśli agent zwróci dane w złym kształcie, np. ujemną kwotę albo nieznaną kategorię, Pydantic je odrzuci, a agent dostanie informację o błędzie i poprawi odpowiedź.*

### 3.2. Przetestuj

Wpisz np.:

> Rano kawa na mieście za 14 zł, potem doładowałam bilet miesięczny za 110, wieczorem kino 32 zł i popcorn za 18.

> Zapłaciłem 230 zł za prąd i 89,99 za internet.

**Ćwiczenie:** zapisuj wydatki do pliku, który otworzysz w Excelu. Na początku pliku dopisz `import csv`, a w pętli, pod linią z `RAZEM`, z tym samym wcięciem:

```python
    with open("wydatki.csv", "a", newline="", encoding="utf-8") as plik:
        zapis = csv.writer(plik)
        for wydatek in wynik.output:
            zapis.writerow([wydatek.co, wydatek.kwota, wydatek.kategoria])
```

*Gotowe rozwiązanie (bez ćwiczenia): [gotowe/krok3_struktura.py](gotowe/krok3_struktura.py)*

## Krok 4. Pamięć rozmowy

W kroku 1 agent zapominał Twoje imię. Model niczego nie pamięta między pytaniami. Żeby „pamiętał”, przy każdym pytaniu wysyłasz mu całą dotychczasową rozmowę.

### 4.1. Trener słówek

Utwórz plik `krok4_pamiec.py`:

```python
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

historia = []

wynik = agent.run_sync("Zaczynamy.", message_history=historia)
historia = wynik.all_messages()
print("Trener:", wynik.output)

while True:
    odpowiedz = input("\nTy: ")
    if odpowiedz.strip().lower() in ("", "koniec"):
        break
    wynik = agent.run_sync(odpowiedz, message_history=historia)
    historia = wynik.all_messages()
    print("Trener:", wynik.output)
```

**Co tu się dzieje:**

- **`historia = []`** to pusta lista na rozmowę.
- **`message_history=historia`** wysyła nowe pytanie razem z całą dotychczasową rozmową.
- **`historia = wynik.all_messages()`** zapamiętuje rozmowę razem z ostatnią odpowiedzią, żeby wysłać ją przy następnym pytaniu.

### 4.2. Przetestuj

Odpowiedz na kilka słówek, raz celowo źle. Sprawdź, czy trener liczy punkty i nie powtarza słów. Potem napisz: „Które słowa pomyliłem?”. Trener powinien pamiętać.

*Im dłuższa rozmowa, tym więcej tekstu idzie do modelu przy każdym pytaniu, więc każde kolejne pytanie trochę więcej kosztuje. Dlatego aplikacje czatowe zaczynają co jakiś czas nową rozmowę.*

**Ćwiczenie:** wróć do `krok1_pierwszy_agent.py` i dodaj pamięć tak samo jak tutaj. Powtórz test z imieniem z kroku 1.3.

*Gotowe rozwiązanie: [gotowe/krok4_pamiec.py](gotowe/krok4_pamiec.py)*

## Krok 5. Czat w przeglądarce

Terminal wystarcza do nauki, ale wygodniej rozmawia się w oknie czatu. Pydantic AI ma wbudowany czat w przeglądarce: ten sam, którego używałeś na warsztacie.

### 5.1. Mistrz gry

Model nie potrafi naprawdę losować: poproszony o rzut kostką, wybiera liczbę, która mu „pasuje”. Dlatego ten agent rzuca prawdziwą kostką przez narzędzie.

Utwórz plik `krok5_czat.py`:

```python
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


app = agent.to_web()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7932)
```

**Co tu się dzieje:**

- **`Field(default=20, ge=2, le=100)`**: domyślnie kostka ma 20 ścianek, a agent może wybrać od 2 do 100. Innej liczby Pydantic nie przepuści.
- **`agent.to_web()`** zamienia agenta w aplikację z oknem czatu. Czat sam pamięta rozmowę, więc lista `historia` z kroku 4 nie jest potrzebna.
- **`uvicorn.run(...)`** uruchamia tę aplikację na Twoim komputerze pod adresem `127.0.0.1`, na porcie `7932`.

### 5.2. Uruchom i zagraj

```bash
python krok5_czat.py
```

Gdy w terminalu pojawi się linia `Uvicorn running on http://127.0.0.1:7932`, otwórz ten adres w przeglądarce i napisz np. „Zaczynamy. Jestem złodziejką w portowym mieście.”.

Czat pokazuje, kiedy agent użył narzędzia `rzut_kostka` i jaki wypadł wynik. Sprawdź, czy opis skutku pasuje do rzutu.

**Terminal musi zostać otwarty**, dopóki korzystasz z czatu. Po zmianie w pliku wciśnij w terminalu Ctrl+C i uruchom plik ponownie.

*Gotowe rozwiązanie: [gotowe/krok5_czat.py](gotowe/krok5_czat.py)*

## Co dalej: Twój własny agent

Znasz już wszystkie elementy. Własnego agenta złożysz z nich tak:

1. **Wybierz jedno zadanie.** Agent do wszystkiego działa gorzej niż agent do jednej rzeczy.
2. **Napisz instrukcję:** kim jest agent, jak ma odpowiadać, kiedy ma dopytać, czego ma nie robić.
3. **Dodaj narzędzia** do wszystkiego, czego model nie wie albo w czym się myli: dzisiejsza data, dane z internetu, rachunki, losowanie, Twoje pliki.
4. **Jeśli wynik ma trafić dalej**, np. do arkusza, ustal jego kształt przez `output_type`.
5. **Wybierz sposób rozmowy:** pętla w terminalu z `message_history` albo czat przez `to_web()`.
6. **Przetestuj** jak na warsztacie: przygotuj kilka pytań, zapisz, czego oczekujesz, i zmieniaj jedną rzecz naraz.

Pomysły na start: asystent do planowania posiłków na tydzień, pomocnik do nauki do egzaminu, agent, który streszcza artykuły spod linku (narzędzie `czytaj_strone` z warsztatu).

**Dokumentacja Pydantic AI:** [pydantic.dev/docs/ai](https://pydantic.dev/docs/ai/overview/). Szczególnie przydadzą się rozdziały o [narzędziach](https://pydantic.dev/docs/ai/tools-toolsets/tools/) i o [kształcie odpowiedzi](https://pydantic.dev/docs/ai/core-concepts/output/).

## Gdy coś nie działa

| Objaw | Co zrobić |
|---|---|
| `python` albo `pip` nie jest rozpoznawane, `ModuleNotFoundError` | Środowisko nie jest aktywne. Na początku wiersza musi być `(.venv)`. Powtórz polecenie z `activate` z kroku 0.3. |
| `running scripts is disabled on this system` (Windows) | Wpisz `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` i powtórz `.venv\Scripts\Activate.ps1`. |
| `can't open file ... No such file or directory` | Plik nie jest zapisany w folderze, w którym jesteś w terminalu, albo nazwa się różni. Wpisz `ls` i sprawdź. |
| Błąd 401, 402 albo 429 | Problem z kluczem albo saldem. Sprawdź tabelę na końcu [KLUCZ-API.md](KLUCZ-API.md). |
| `IndentationError` | Złe wcięcie. Terminal podaje numer linii. Wcięcia rób czterema spacjami. |
| `SyntaxError` | Najczęściej brakujący cudzysłów, nawias albo dwukropek na końcu linii z `while`, `if`, `def`. |
| `NameError: name '...' is not defined` | Literówka w nazwie albo brakujący `import` na początku pliku. Porównaj z plikiem z folderu `gotowe/`. |
| `UnexpectedModelBehavior: Tool '...' exceeded max retries` | Narzędzie kilka razy z rzędu zwróciło błąd, np. przez brak internetu albo zły kod waluty, i program się zatrzymał. Sprawdź połączenie, uruchom plik ponownie i zapytaj inaczej. |
| `Address already in use` (krok 5) | Czat już działa w innym oknie terminala. Zamknij tamto okno albo wciśnij w nim Ctrl+C. |
| Agent nie używa narzędzia, tylko zgaduje | Doprecyzuj opis narzędzia i instrukcję, np. „Kursy sprawdzaj zawsze narzędziem…”. |
