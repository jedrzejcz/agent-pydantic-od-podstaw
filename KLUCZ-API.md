# Własny klucz API do OpenRoutera

Na warsztacie korzystasz z klucza od prowadzącego. Po warsztacie ten klucz przestanie działać. Żeby dalej używać swojego asystenta, potrzebujesz własnego klucza. Ta instrukcja pokazuje, skąd go wziąć, ile to kosztuje i jak go bezpiecznie przechowywać.

**Czym jest OpenRouter?** To pośrednik między Twoim asystentem a modelami AI różnych firm (OpenAI, Anthropic, Google, Meta, Mistral i innych). Masz jedno konto, jeden klucz i jedno saldo, a model zmieniasz jedną linijką w kodzie.

**Potrzebujesz:**

- adresu e-mail albo konta Google lub GitHub do rejestracji,
- karty płatniczej, jeśli chcesz korzystać z modeli płatnych (np. `openai/gpt-5`, którego używa asystent z warsztatu). Modele darmowe działają bez karty, ale z limitami (patrz niżej).

## Część 1. Załóż konto i utwórz klucz

### 1. Zarejestruj się

Wejdź na [openrouter.ai](https://openrouter.ai), kliknij **Sign in** w prawym górnym rogu i załóż konto e-mailem, kontem Google albo GitHub.

### 2. Doładuj konto (tylko dla modeli płatnych)

Wejdź na stronę [openrouter.ai/settings/credits](https://openrouter.ai/settings/credits) i kliknij **Add Credits**. Wpisz kwotę i zapłać kartą.

- Saldo jest w dolarach: 1 kredyt to 1 USD.
- Przy płatności kartą OpenRouter dolicza opłatę 5,5% (co najmniej 0,80 USD).
- Niewykorzystane kredyty mogą wygasnąć po roku od zakupu.

*Na naukę i testy w zupełności wystarczy 5–10 USD. Doładowanie łącznie co najmniej 10 USD ma dodatkową zaletę: podnosi dzienny limit darmowych modeli z 50 do 1000 zapytań.*

### 3. Utwórz klucz

Wejdź na stronę [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys) i kliknij **Create Key**.

1. W polu nazwy wpisz, do czego służy klucz, np. `asystent-domowy`. Nazwa pomoże Ci później rozpoznać klucz na liście.
2. Ustaw **limit kredytów** (credit limit), np. 5 USD. Po jego wyczerpaniu klucz przestaje działać, dopóki nie podniesiesz limitu. Limit może też odnawiać się co dzień, tydzień albo miesiąc.
3. Kliknij **Create**.

Klucz zaczyna się od `sk-or-v1-`. **Skopiuj go od razu**: OpenRouter pokazuje go tylko raz. Jeśli go zgubisz, nie odzyskasz go. Usuń wtedy stary klucz i utwórz nowy.

*Limit na kluczu to Twój bezpiecznik. Jeśli klucz wycieknie albo asystent wpadnie w pętlę zapytań, stracisz najwyżej tyle, ile wynosi limit, a nie całe saldo.*

### 4. Wklej klucz do asystenta

W folderze z asystentem otwórz plik `.env` (jeśli go nie ma, skopiuj `.env.example` jako `.env`) i wpisz swój klucz:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

Bez spacji i bez cudzysłowów. Zapisz plik i uruchom asystenta ponownie.

## Część 2. Ile to kosztuje i jak wybrać model

### Modele płatne

Płacisz za tokeny, czyli za kawałki tekstu: osobno za tekst wysłany do modelu (input) i za odpowiedź (output). Ceny są podane za milion tokenów i różnią się między modelami nawet kilkudziesięciokrotnie. Aktualną cenę znajdziesz na stronie każdego modelu na liście [openrouter.ai/models](https://openrouter.ai/models).

Model zmieniasz w kodzie agenta. W asystencie z warsztatu jest to linia z `MODEL` w `agent.py`:

```python
MODEL = "openrouter:openai/gpt-5"
```

Część po `openrouter:` to nazwa modelu skopiowana z jego strony na OpenRouterze.

Dla porównania ceny trzech modeli OpenAI (za milion tokenów, stan na październik 2026):

| Model | Tekst wysłany | Odpowiedź |
|---|---|---|
| `openai/gpt-5` | 1,25 USD | 10,00 USD |
| `openai/gpt-5-mini` | 0,25 USD | 2,00 USD |
| `openai/gpt-5-nano` | 0,05 USD | 0,40 USD |

*Do nauki w domu wystarczy w zupełności `openai/gpt-5-mini`: jest pięć razy tańszy od `gpt-5` i dobrze radzi sobie z narzędziami.*

*Asystent z narzędziami wysyła do modelu więcej tekstu, niż widzisz w czacie: instrukcję, opisy narzędzi i ich wyniki. Jedna rozmowa może więc kosztować więcej, niż wynikałoby z długości samych wiadomości.*

### Modele darmowe

Nazwy darmowych modeli kończą się na `:free`. Znajdziesz je, wpisując `free` w wyszukiwarkę na [openrouter.ai/models](https://openrouter.ai/models). Mają limity:

| Łącznie kupione kredyty | Zapytań na minutę | Zapytań na dzień |
|---|---|---|
| mniej niż 10 USD | 20 | 50 |
| co najmniej 10 USD | 20 | 1000 |

*Asystent z narzędziami zużywa kilka zapytań na jedno pytanie (osobno na każde wywołanie narzędzia), więc limit 50 dziennie kończy się szybciej, niż się wydaje. Nie każdy darmowy model obsługuje też narzędzia: na liście modeli włącz filtr **Supported Parameters → tools**.*

### Gdzie sprawdzić wydatki

Na stronie [openrouter.ai/activity](https://openrouter.ai/activity) widzisz każde zapytanie: model, liczbę tokenów i koszt. Zajrzyj tam po pierwszych testach, żeby wiedzieć, ile kosztuje Cię typowa rozmowa.

## Część 3. Bezpieczeństwo klucza

Klucz działa jak karta płatnicza podpięta do Twojego salda. Kto go ma, ten wydaje Twoje pieniądze.

- **Trzymaj klucz tylko w pliku `.env`.** Nie wpisuj go w kod agenta.
- **Nie wysyłaj pliku `.env` nikomu** i nie wrzucaj go do repozytorium. Plik `.gitignore` w repozytoriach z warsztatu już go pomija, ale sprawdź to, jeśli zakładasz własny projekt.
- **Nie wklejaj klucza w czaty, maile ani zrzuty ekranu.**
- **Ustaw limit na każdym kluczu** (krok 3).
- **Jeden klucz na jeden projekt.** Gdy coś wycieknie, usuwasz jeden klucz, a reszta działa dalej.

Jeśli podejrzewasz, że klucz wyciekł: wejdź na [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys), usuń go i utwórz nowy. OpenRouter skanuje też publiczne repozytoria na GitHubie i wysyła e-mail, gdy znajdzie tam Twój klucz.

## Gdy coś nie działa

| Objaw | Co zrobić |
|---|---|
| Błąd 401 | Klucz jest błędny, usunięty albo źle wklejony. Sprawdź plik `.env`: bez spacji, bez cudzysłowów, cały klucz od `sk-or-v1-`. |
| Błąd 402 | Brak środków: saldo jest ujemne albo klucz wyczerpał swój limit. Doładuj konto albo podnieś limit klucza. Przy ujemnym saldzie nie działają nawet modele darmowe. |
| Błąd 429 | Za dużo zapytań. Przy modelu darmowym odczekaj minutę albo do następnego dnia, doładuj łącznie co najmniej 10 USD albo przejdź na model płatny. |
| Asystent nie używa narzędzi albo zgłasza przy nich błąd | Wybrany model nie obsługuje narzędzi. Wybierz inny. |
| Zmieniłem klucz, a nic się nie zmieniło | Zapisz `.env` i uruchom asystenta ponownie: Ctrl+C w terminalu, potem znowu `python` i nazwa pliku. |

*Stan na październik 2026. Ceny, opłaty i limity mogą się zmienić; aktualne znajdziesz w [dokumentacji OpenRoutera](https://openrouter.ai/docs).*
