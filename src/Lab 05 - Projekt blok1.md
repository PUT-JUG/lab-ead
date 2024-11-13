# Lab 05 - Projekt podsumowujący biblioteki Pandas i Matplotlib

## Cel projektu
Celem projektu jest utrwalenie wiedzy dotyczącej pobierania i wczytywania danych oraz biblioteki Pandas.
W celu realizacji części zadań zapoznaj się z przykładami i informacjami dotyczącymi przetwarzania danych tabelarycznych w tym mechanizmu wieloindeksowania. W zadaniach wystarczające jest wykorzystanie metody tabeli przestawnej (`pivot_table`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html) lub/i metody grupowania (`groupby`). Przydatnymi metodami wykorzystywanymi w dalszej części zajęć będą też metoda dyskretyzacji `cut`, faktoryzacji (`factorize`), oraz wyznaczanie częstości wystąpień i normalizacji (`crosstab`)
Informacje na ten temat możesz znaleźć [tutaj](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)

## Opis zadania
Na stronie Social Security Administration umieszczono dane zawierającą listę imion oraz częstotliwość ich występowania w latach 1880-2023. Pliki z danymi w formacie CSV dostępne są [tutaj](https://www.ssa.gov/oact/babynames/names.zip).

1. Wczytaj dane ze wszystkich plików do pojedynczej tablicy (używając Pandas).
2. Określi ile różnych (unikalnych) imion zostało nadanych w tym czasie.
3. Określi ile różnych (unikalnych) imion zostało nadanych w tym czasie rozróżniając imiona męskie i żeńskie.
4. Stwórz nowe kolumny `frequency_male` i `frequency_female` i określ popularność każdego z imion w danym każdym roku dzieląc liczbę razy, kiedy imię zostało nadane przez całkowita liczbę urodzeń dla danej płci.  
5. Określ i wyświetl wykres złożony z dwóch podwykresów, gdzie osią x jest skala czasu, a oś y reprezentuje:
   - liczbę urodzin w danym roku (wykres na górze)
   - stosunek liczby narodzin dziewczynek do liczby narodzin chłopców w każdym roku(wykres na dole)
W którym roku zanotowano najmniejszą, a w którym największą różnicę w liczbie urodzeń między chłopcami a dziewczynkami (pytanie dotyczy podwykresu przedstawiającego stosunek liczby urodzin)? Odpowiedź wyznacz i  wyświetl  na ekranie
6. Wyznacz 1000 najpopularniejszych imion dla każdej płci w całym zakresie czasowym, metoda powinna polegać na wyznaczeniu 1000 najpopularniejszych imion dla każdego roku i dla każdej płci osobno. Jako najpopularniejsze należy uznać imiona, które najdłużej zajmowały wysokie miejsce na liście rankingowej, żeby uniknąć wpływu liczny urodzin w danym roku na wynik (liczba urodzin spada stąd, nieprawidłowo przeprowadzona procedura może powodować że imiona nadawane w wyżu i stosowane w tym czasie zdominują ranking) proszę ranking Top1000 określić jako sumę ważoną względnej popularności danego imienia w danym roku (patrz pkt 4)
7. Wyświetl na jednym wykresie zmiany dla imienia męskiego *John* i  pierwszego imienia żeńskiego rankingu top-1000 (zaopatrz wykres w odpowiednią legendę):
    - na osi Y po lewej liczbę razy kiedy imę zostało nadane w każdym roku (wyświetl ile razy nadano to imię w 1934, 1980 i 2022r)?
    - na osi Y po prawej popularność tych imion w każdym z tych lat
8. Wykreśl wykres z podziałem na lata i płeć zawierający informację jaki procent w danym roku stanowiły imiona należące do rankingu top1000 (wyznaczonego dla całego zbioru (pkt 6)). Wykres ten powinien przedstawiać zmianę różnorodności imion w kolejnych latach z podziałem na płeć. Zaznacz na wykresie oraz wyświetl w konsoli rok, w którym zaobserwowano największą różnicę w różnorodności między imionami męskimi a żeńskimi. Odpowiedz na pytanie wyświetlając odpowiedni tekst w skrypcie: "Co zmieniło się na przestrzeni ostatnich 140 lat jeśli chodzi o różnorodność imion? czy różnorodność zależy od płci?"
9. Zweryfikuj hipotezę czy prawdą jest, że w obserwowanym okresie rozkład ostatnich liter imion męskich uległ istotnej zmianie? W tym celu 
    - dokonaj agregacji wszystkich urodzeń w pełnym zbiorze danych z podziałem na rok i płeć i ostatnią literę,
    - wyodrębnij dane dla lat 1910, 1970, 2023
    - znormalizuj dane względem całkowitej liczby urodzin w danym roku
    - wyświetl dane popularności litery dla mężczyzn w postaci wykresu słupkowego zawierającego poszczególne lata i gdzie słupki grupowane są wg litery. Wyświetl, dla której litery wystąpił największy wzrost/spadek między rokiem 1910 a 2023)
    - Dla 3 liter dla których zaobserwowano największą zmianę wyświetl przebieg trendu popularności w całym okresie  czasu
10.  Znajdź w rankingu top1000 imiona, które nadawane były zarówno dziewczynkom jak i chłopcom (stosunek nadanych imion męskich i żeńskich). Wyznacz 2 imiona (jedno które z kiedyś było typowo męskie a aktualnie jest imieniem żeńskim i drugie które kiedyś było typowo żeńskim a aktualnie jest typowo męskim). Typowo męskie imię to takie dla którego iloraz imion nadawanych chłopcom do całkowitej liczby imion jest bliski 1 (`p_m`), analogicznie iloraz można zdefiniować dla dziewczynek (`p_k`). Największa zmiana między rokiem X a rokiem Y może być zdefiniowana jako średnia z sumy `(p_m(X)+p_k(Y))/2`. Do analizy zmiany konotacji imienia wykorzystaj 2 przedziały: zagregowane dane do roku 1920 i od roku 2000. 
     - wyświetl te imiona
     - wkreśl przebieg trendu dla tych imion obrazujący zmianę konotacji danego imienia na przestrzeni lat

11. Imiona w Polsce
    
    Celem tej części jest zastosowanie stworzonych mechanizmów dla datasetu zawierającego imiona nadawane w Polsce w latach 2000-2023. Spróbuj w ten sposob tworzyć funkcje, żeby można było je wykorzystywać dla obu datasetów. Oczywiście przy wczytywaniu mozesz dokonać z transformacji struktury tabel i nazw kolumn, tak, żeby uzyskać spójność zgodność między datasetami.
    1.  Wczytaj z bazy [imiona_pl](https://chmura.put.poznan.pl/s/WIP4dBFsVTzLrKA) zestaw danych zawierający liczbę nadawanych imion w okresie 2000-2023 w Polsce.
    - zapytanie sql powinno tworzyć pojedynczą tabelę, zawierającą imię, rok, oraz liczbę nadanych imion dla dziewczynek i chłopców. W bazie są 2 oddzielne tabele dla każdej z płci.
    1. Stwórz ranking top 200 imion i porównaj czy obserwacje z pkt. 8 dotyczące trendów w nadawaniu imion w USA są również obserwowalne w Polsce. Jako daty referencyjne weź rok 2000, 2013, 2023. Stosując histogram spróbuj odpowiedzieć na pytanie co zmieniło się między rokiem 2000 a 2013 czy zmiana w trendzie wynika tylko z zmiany zwyczajów czy też innych czynników
    2. Znajdź 2 imiona, które stosunkowo czesto nadawane były dziewczynkom i chłopcom

*Uwagi:*
- jako rozwiązanie prześlij skrypt - pojedynczy plik `py`. Pliki wejściowe (dane w zadaniu) powinny być zaczytywane ścieżką względną z podkatalogu `./data`. 
- przed przesłanie rozwiązania proszę zweryfikować czy skrypt się uruchamia. (skrypty z błędami nie będą analizowane)
- w komentarzach umieść informację o zadaniu, którego dotyczy dana część kodu
- kody będą poddane analizie antyplagaitowej



---
Autorzy: *Piotr Kaczmarek* 
