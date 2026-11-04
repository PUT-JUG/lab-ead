# Lab 05 - Projekt podsumowujący biblioteki Pandas i Matplotlib

## Cel projektu
Celem projektu jest utrwalenie wiedzy dotyczącej pobierania i wczytywania danych (pliki, baza SQL) oraz bibliotek Pandas i Matplotlib.
W celu realizacji części zadań zapoznaj się z przykładami i informacjami dotyczącymi przetwarzania danych tabelarycznych, w tym mechanizmu wieloindeksowania. W zadaniach wystarczające jest wykorzystanie metody tabeli przestawnej (`pivot_table`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html) lub/i metody grupowania (`groupby`, `transform`, `rank`). Przydatnymi metodami będą też metoda dyskretyzacji `cut`, faktoryzacji (`factorize`) oraz wyznaczanie częstości wystąpień i normalizacji (`crosstab` lub `pivot_table`).
Informacje na ten temat możesz znaleźć [tutaj](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html).

## Przygotowanie

Pliki potrzebne do projektu znajdują się w katalogu [projekt1](_resources/projekt1/):

- [`projekt1_szablon.py`](_resources/projekt1/projekt1_szablon.py) - szablon rozwiązania z wymaganymi funkcjami i ich specyfikacją,
- [`parametry.py`](_resources/projekt1/parametry.py) - generator Twoich indywidualnych parametrów,
- [`test_public.py`](_resources/projekt1/test_public.py) - testy publiczne do samodzielnego sprawdzenia rozwiązania.

### Parametry indywidualne
Część wartości w zadaniach (wielkości rankingów, progi, lata) jest inna dla każdego studenta i zależy od numeru indeksu. Wygeneruj je poleceniem:

```bash
python parametry.py 123456
```

i wklej wynik (`STUDENT_ID` i `PARAMS`) na początek swojego skryptu. W treści zadań parametry oznaczone są jako `PARAMS["nazwa"]`. Rozwiązanie wykonane dla cudzych parametrów jest oceniane jako niepoprawne.

### Wymagana struktura rozwiązania
Rozwiązanie jest sprawdzane automatycznie, dlatego musi zachować strukturę szablonu:

- funkcje opisane w szablonie jako WYMAGANE muszą mieć dokładnie takie nazwy, argumenty i zwracane wartości, jak w ich opisie (docstringu); mogą korzystać z dowolnych własnych funkcji pomocniczych,
- funkcje wymagane tylko liczą - nie rysują, nie wyświetlają i nie modyfikują przekazanych ramek danych,
- cały skrypt uruchamia się przez `main()` (`if __name__ == "__main__": main()`),
- `main()` zapisuje do katalogu `./wyniki` plik `results.json` o strukturze podanej w szablonie oraz wykresy `fig_04.png`, `fig_06.png`, `fig_07.png`, `fig_08a.png`, `fig_08b.png`, `fig_09.png`, `fig_10a.png`, `fig_10b.png` (numer = numer zadania),
- odpowiedzi na pytania opisowe umieść w `results["answers"]` (i wyświetl w konsoli),
- dozwolone biblioteki: biblioteka standardowa Pythona, `numpy`, `pandas`, `matplotlib`, `seaborn`, `duckdb`; skrypt jest uruchamiany w Pythonie 3.12 z pandas 3.x, bez dostępu do internetu.

Przed oddaniem uruchom testy publiczne (z katalogu, w którym jest skrypt i podkatalog `./data`):

```bash
python test_public.py moj_projekt.py --full
```

Zaliczenie testów publicznych jest warunkiem koniecznym, ale nie wystarczającym - przy ocenie funkcje są dodatkowo sprawdzane na innych danych (np. nieposortowanych, z remisami i lukami w latach).

## Opis zadania
Na stronie Social Security Administration umieszczono dane zawierające listę imion oraz częstotliwość ich występowania w latach 1880-2025. Pliki z danymi dostępne są [tutaj](https://www.ssa.gov/oact/babynames/names.zip). Archiwum zawiera pliki `yobRRRR.txt` (po jednym dla każdego roku) w formacie CSV **bez nagłówka**, z kolumnami: imię, płeć (`F`/`M`), liczba nadań. Rok należy odczytać z nazwy pliku.

W całym zadaniu przez *liczbę urodzeń* rozumiemy sumę liczby nadanych imion w danym roku (dla danej płci lub łącznie), wyznaczoną na podstawie zbioru danych. Przy remisach (np. dwa lata z tą samą wartością) wybieraj pierwszą wartość: najwcześniejszy rok, imię wyżej w rankingu.

### Część I - imiona w USA

1. Wczytaj dane ze wszystkich plików do pojedynczej ramki danych (używając Pandas lub DuckDB), dodając kolumny z rokiem oraz dekadą (np. 1987 → 1980). Dane posortuj wg roku rosnąco, a w obrębie roku wg płci i malejąco wg liczby nadań - nie zakładaj, że kolejność plików jest odpowiednia. *(funkcja `load_usa`)*
2. Wyznacz i wyświetl *(funkcja `name_stats`)*:
    - liczbę różnych (unikalnych) imion w całym zbiorze - łącznie (imię nadawane obu płciom liczymy raz) oraz osobno dla każdej płci,
    - liczbę imion (osobno dla każdej płci), które pojawiły się w zbiorze tylko w jednym roku,
    - liczbę nowych imion w każdej dekadzie, czyli imion, które pojawiły się w zbiorze po raz pierwszy w danej dekadzie (bez rozróżnienia płci).
3. Dla każdego wiersza (imię, płeć, rok) wyznacz *(funkcja `add_frequency_rank`)*:
    - `frequency` - popularność imienia, czyli liczbę nadań podzieloną przez liczbę urodzeń danej płci w danym roku,
    - `rank` - pozycję imienia w rankingu danego roku i danej płci (1 = najczęściej nadawane; imiona o tej samej liczbie nadań otrzymują tę samą, najniższą pozycję).

    Nie używaj pętli po latach - wykorzystaj operacje grupowania.
4. Wyświetl wykres złożony z dwóch podwykresów ze wspólną osią czasu (x), gdzie oś y reprezentuje *(funkcja `unique_per_year`)*:
    - liczbę unikalnych imion nadanych w danym roku, osobno dla każdej płci (wykres na górze),
    - stosunek liczby unikalnych imion żeńskich do liczby unikalnych imion męskich w danym roku (wykres na dole).

    Zaznacz na dolnym wykresie rok, w którym stosunek był najmniejszy, oraz rok, w którym był największy, umieszczając przy nich opis tekstowy z rokiem i wartością.
5. Wyznacz ranking top-`PARAMS["top_n"]` imion osobno dla każdej płci. Kryterium jest **szczytowa popularność**, czyli maksymalna wartość `frequency` (pkt 3) osiągnięta przez imię w dowolnym roku. Dla każdego imienia zapisz także rok, w którym osiągnęło szczyt. Wyświetl po 5 pierwszych imion każdej płci wraz z wartością szczytu i rokiem szczytu. *(funkcja `peak_ranking`)*
6. Wyświetl na jednym wykresie przebieg w czasie dla dwóch imion:
    - imienia żeńskiego zajmującego 1. miejsce w rankingu z pkt 5,
    - imienia męskiego, które spośród `PARAMS["top_k_male"]` pierwszych imion męskich rankingu z pkt 5 osiągnęło szczyt popularności najpóźniej.

    Wykres powinien zawierać:
    - na osi Y po lewej - liczbę nadań imienia w każdym roku,
    - na osi Y po prawej - popularność (`frequency`) imienia w każdym roku,
    - zaznaczony punkt szczytu popularności każdego z imion z opisem (rok, liczba nadań) oraz opis z liczbą nadań w roku `PARAMS["annot_year"]`,
    - legendę opisującą wszystkie serie (z obu osi).
7. Różnorodność imion: dla każdego roku i każdej płci wyznacz, ile najpopularniejszych imion potrzeba, aby łącznie pokryły one co najmniej `PARAMS["coverage_q"]` (udział) urodzeń danej płci w danym roku *(funkcja `coverage`)*. Wykreśl wynik w funkcji czasu z podziałem na płeć. Zaznacz na wykresie oraz wyświetl w konsoli rok, w którym różnica tej miary między dziewczynkami a chłopcami (wartość bezwzględna) była największa. Odpowiedz na pytanie: "Jak zmieniała się różnorodność imion w latach 1880-2025? Czy różnorodność zależy od płci?"
8. Długość imion: zweryfikuj hipotezę, że w obserwowanym okresie nadawane imiona stały się dłuższe. W tym celu:
    - wyznacz średnią długość imienia (liczbę liter) w każdym roku z podziałem na płeć, ważoną liczbą nadań, i przedstaw ją na wykresie liniowym *(funkcja `mean_name_length`)*,
    - dla płci `PARAMS["length_sex"]` wyznacz rozkład długości imion (udział urodzeń dla każdej długości imienia, znormalizowany względem liczby urodzeń w danym roku) dla lat `PARAMS["length_years"]` i przedstaw go na wykresie słupkowym, w którym słupki grupowane są wg długości imienia, a w każdej grupie znajduje się słupek dla każdego z lat *(funkcja `length_distribution`)*,
    - wyświetl, dla której długości imienia wystąpił największy wzrost, a dla której największy spadek udziału między pierwszym a ostatnim rokiem z `PARAMS["length_years"]`.
9. Zmiana konotacji imion: rozważ imiona, które należą jednocześnie do rankingu imion żeńskich i rankingu imion męskich z pkt 5. Dla każdego z nich i każdej dekady wyznacz wskaźnik `w_m` - stosunek liczby nadań męskich do łącznej liczby nadań imienia w tej dekadzie. Pomiń dekady, w których imię nadano łącznie mniej niż `PARAMS["min_decade_births"]` razy *(funkcja `decade_connotation`)*. Następnie:
    - wyznacz zmianę `w_m` między kolejnymi uwzględnionymi dekadami dla każdego imienia,
    - wyświetl imię i dekadę, dla których zaobserwowano największy spadek `w_m` (najszybsza zmiana w kierunku imienia żeńskiego), oraz imię i dekadę, dla których zaobserwowano największy wzrost `w_m` (najszybsza zmiana w kierunku imienia męskiego),
    - dla tych dwóch imion wykreśl przebieg `w_m` w każdym roku (nie w dekadach) w całym okresie.

### Część II - imiona w Polsce

Celem tej części jest zastosowanie stworzonych mechanizmów dla zbioru danych zawierającego imiona nadawane w Polsce w latach 2000-2025. Funkcje z części I powinny działać dla obu zbiorów danych bez modyfikacji (dopuszczalne są różne wartości parametrów).

10. Imiona w Polsce:
    - Wczytaj z bazy [imiona_pl](https://chmura.put.poznan.pl/s/3EG4w9eoQtRNLAZ) (plik SQLite `names_pl_2000-25.sqlite`) dane o liczbie nadanych imion w Polsce. W bazie są 2 oddzielne tabele, po jednej dla każdej płci (`males`, `females`). Pojedyncze zapytanie SQL powinno zwracać jedną tabelę w takiej samej postaci jak ramka danych z części I (imię, płeć `F`/`M`, rok, liczba nadań), uzupełnioną o kolumnę z popularnością (`frequency`) **wyznaczoną w samym zapytaniu SQL** *(funkcja `load_pl`)*. Sprawdź, czy wartości `frequency` z SQL są zgodne z wynikiem funkcji z pkt 3.
    - Wyznacz ranking top-`PARAMS["pl_top_n"]` imion (osobno dla każdej płci) metodą z pkt 5 i wyświetl po 5 pierwszych imion każdej płci wraz z rokiem szczytu oraz ostatnie imię rankingu.
    - Dla danych polskich wyznacz dwie miary różnorodności: liczbę unikalnych imion w danym roku (pkt 4) oraz liczbę imion pokrywających udział `PARAMS["coverage_q"]` urodzeń (pkt 7). Przedstaw obie miary na jednym wykresie (z podziałem na płeć). Czy obie miary pokazują ten sam trend? Zwróć szczególną uwagę na okres 2000-2013 i odpowiedz na pytanie: czy zmiana w trendzie wynika tylko ze zmiany zwyczajów, czy też z innych czynników (czy potrafisz zidentyfikować te czynniki?). Czy trendy różnorodności z pkt 7 obserwowane w USA są widoczne również w Polsce?
    - Porównaj średnią ważoną długość imion (pkt 8) w Polsce i w USA w latach 2000-2025 na jednym wykresie (4 serie: kraj × płeć). Czy w obu krajach zmiany idą w tym samym kierunku?


## *Uwagi:*
- jako rozwiązanie prześlij skrypt - pojedynczy plik `py` zgodny z szablonem. Pliki wejściowe powinny być wczytywane ścieżką względną z podkatalogu `./data`, w którym znajdują się rozpakowane pliki źródłowe z imionami (`yobRRRR.txt`) oraz baza danych `names_pl_2000-25.sqlite`.
- skrypty, które nie uruchamiają się (błąd, brak wymaganej struktury), nie będą analizowane - użyj `test_public.py --full`.
- w komentarzach umieść informację o zadaniu, którego dotyczy dana część kodu.
- kody będą poddane analizie antyplagiatowej (również względem rozwiązań z poprzednich lat).

## Samodzielność i obrona
Korzystanie z dokumentacji, materiałów z zajęć i narzędzi AI jako pomocy jest dozwolone choć głównym celem projektu jest samodzielne opracowanie rozwiązania i nauka korzystania z tych narzędzi, stąd też wymagana jest umiejętność obrony swojego rozwiązania. Pamiętaj, że ocenie podlega Twoje zrozumienie rozwiązania. Wybrane osoby (w tym wszystkie, których prace wykazują duże podobieństwo do innych prac lub budzą wątpliwości co do samodzielności) zostaną poproszone o krótką obronę (5-7 min): omówienie fragmentu kodu i wprowadzenie w nim na bieżąco niewielkiej zmiany (np. innego kryterium rankingu lub progu). Ocena z projektu jest mnożona przez wynik obrony (0 / 0,5 / 1).

**Kryteria oceny:**

- **Zgodność z wymaganiami zadania (60%)** - poprawność wyników (`results.json`) i funkcji (testy automatyczne), kompletność i czytelność wykresów, odpowiedzi na pytania
- **Jakość i organizacja kodu (20%)** - zastosowanie dobrych praktyk programistycznych:
  - refaktoryzacja i modularność kodu
  - parametryzacja zamiast wartości zhardcodowanych
  - ponowne wykorzystanie funkcji w różnych kontekstach (w szczególności dla obu zbiorów danych)
  - czytelność i dokumentacja kodu
- **Wydajność i optymalizacja (20%)** - efektywne wykorzystanie narzędzi:
  - czas wykonania całego skryptu (mierzony automatycznie)
  - zastosowanie operacji wektoryzowanych
  - wykorzystanie zaawansowanych funkcjonalności bibliotek Pandas, Matplotlib i DuckDB

---
Autorzy: *Piotr Kaczmarek*
