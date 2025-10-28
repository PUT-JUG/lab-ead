# Lab 05 - Projekt podsumowujący biblioteki Pandas i Matplotlib

## Cel projektu
Celem projektu jest utrwalenie wiedzy dotyczącej pobierania i wczytywania danych oraz biblioteki Pandas.
W celu realizacji części zadań zapoznaj się z przykładami i informacjami dotyczącymi przetwarzania danych tabelarycznych w tym mechanizmu wieloindeksowania. W zadaniach wystarczające jest wykorzystanie metody tabeli przestawnej (`pivot_table`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html) lub/i metody grupowania (`groupby`). Przydatnymi metodami wykorzystywanymi w dalszej części zajęć będą też metoda dyskretyzacji `cut`, faktoryzacji (`factorize`), oraz wyznaczanie częstości wystąpień i normalizacji (`crosstab`)
Informacje na ten temat możesz znaleźć [tutaj](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)

## Opis zadania
Na stronie Social Security Administration umieszczono dane zawierającą listę imion oraz częstotliwość ich występowania w latach 1880-2023. Pliki z danymi w formacie CSV dostępne są [tutaj](https://www.ssa.gov/oact/babynames/names.zip).

1. Wczytaj dane ze wszystkich plików do pojedynczej tablicy (używając Pandas lub DuckDB).
2. Określi ile różnych (unikalnych) imion zostało nadanych w tym czasie.
3. Określi ile różnych (unikalnych) imion zostało nadanych w tym czasie rozróżniając imiona męskie i żeńskie.
4. Stwórz nowe kolumny `frequency_male` i `frequency_female` i określ popularność każdego z imion w danym każdym roku dzieląc liczbę razy, kiedy imię zostało nadane przez całkowita liczbę urodzeń dla danej płci.  
5. Określ i wyświetl wykres złożony z dwóch podwykresów, gdzie osią x jest skala czasu, a oś y reprezentuje:
   - liczbę urodzin w danym roku (wykres na górze)
   - stosunek liczby narodzin dziewczynek do liczby narodzin chłopców w każdym roku(wykres na dole)
W którym roku zanotowano najmniejszą, a w którym największą różnicę w liczbie urodzeń między chłopcami a dziewczynkami (pytanie dotyczy podwykresu przedstawiającego stosunek liczby urodzin)? Odpowiedź wyznacz i  wyświetl  na wykresie wskazując na wykresie odpowiednią wartość i umieszczając na nim opis tekstowy
6. Wyznacz 1000 najpopularniejszych imion osobno dla każdej płci w całym zakresie czasowym, metoda powinna polegać na wyznaczonych w punkcie 4 wartościach frequency. Jako najpopularniejsze należy uznać imiona, których średnia popularność liczona w całym horyzoncie czasu jest największa.
7. Wyświetl na jednym wykresie zmiany dla drugiego najpopularniejszego imienia męskiego w okresie od 2000r i  pierwszego najpopularniejszego imienia żeńskiego rankingu top-1000 (zaopatrz wykres w odpowiednią legendę):
    - na osi Y po lewej liczbę razy kiedy imię zostało nadane w każdym roku (ponadto wyświetl na wykresie opis wskazujący  ile razy nadano to imię w 1934, 1980 i 2024r)?
    - na osi Y po prawej popularność tych imion w każdym roku 
8. Wykreśl wykres z podziałem na lata i płeć zawierający informację jaki procent w danym roku stanowiły imiona należące do rankingu top1000 (wyznaczonego dla całego zbioru (pkt 6)). Wykres ten powinien przedstawiać zmianę różnorodności imion w kolejnych latach z podziałem na płeć. Zaznacz na wykresie oraz wyświetl w konsoli rok, w którym zaobserwowano największą różnicę w różnorodności między imionami męskimi a żeńskimi. Odpowiedz na pytanie wyświetlając odpowiedni tekst w skrypcie: "Co zmieniło się na przestrzeni ostatnich 144 lat jeśli chodzi o różnorodność imion? czy różnorodność zależy od płci?"
9. Zweryfikuj hipotezę czy prawdą jest, że w obserwowanym okresie rozkład ostatnich liter imion męskich uległ istotnej zmianie? W tym celu 
    - dokonaj agregacji wszystkich urodzeń w pełnym zbiorze danych z podziałem na rok i płeć i ostatnią literę,
    - wyodrębnij dane dla lat 1900, 1975, 2024
    - znormalizuj dane względem całkowitej liczby urodzin w danym roku
    - wyświetl dane popularności litery dla mężczyzn w postaci wykresu słupkowego zawierającego poszczególne lata i gdzie słupki grupowane są wg litery. Wyświetl, dla której litery wystąpił największy wzrost/spadek między rokiem 1900 a 2024
    - Dla 3 liter dla których zaobserwowano największą zmianę wyświetl przebieg trendu popularności w całym okresie  czasu (dla każdego roku)
10.   Znajdź w rankingu top1000 imiona, które nadawane były zarówno dziewczynkom jak i chłopcom (wyznacz stosunek nadanych imion męskich  do całkowitej liczby danego imienia (w_m) oraz analogiczny wskaźnik dla imion żeńskich (w_f)). Wyznacz 2 imiona (jedno które z kiedyś było typowo męskie (wskaźnik w_m~1) a aktualnie jest imieniem żeńskim (wskaźnik w_k~1) i drugie które kiedyś było typowo żeńskim a aktualnie jest typowo męskim). Największa zmiana między rokiem X a rokiem Y może być zdefiniowana jako średnia z sumy `(w_m(X)+w_f(Y))/2`. Do analizy zmiany konotacji imienia wykorzystaj 2 przedziały: zagregowane dane do roku 1920 i od roku 2000. 
     - wyświetl te imiona
     - wkreśl przebieg trendu konotacji dla tych imion obrazujący zmianę konotacji danego imienia na przestrzeni lat
11.  Imiona w Polsce
    
    Celem tej części jest zastosowanie stworzonych mechanizmów dla datasetu zawierającego imiona nadawane w Polsce w latach 2000-2024. Spróbuj w ten sposob tworzyć funkcje, żeby można było je wykorzystywać dla obu datasetów. Oczywiście przy wczytywaniu mozesz dokonać z transformacji struktury tabel i nazw kolumn, tak, żeby uzyskać spójność zgodność między datasetami.
    1.  Wczytaj z bazy [imiona_pl](https://chmura.put.poznan.pl/s/foC9qaKz7B8cQBK) zestaw danych zawierający liczbę nadawanych imion w okresie 2000-2024 w Polsce. Zapytanie sql powinno tworzyć pojedynczą tabelę, zawierającą imię, rok, oraz liczbę nadanych imion dla dziewczynek i chłopców. W bazie są 2 oddzielne tabele dla każdej z płci.
    2. Stwórz ranking top 200 imion i porównaj czy obserwacje z pkt. 8 dotyczące trendów w nadawaniu imion w USA są również obserwowalne w Polsce. Jako daty referencyjne weź rok 2000, 2013, 2024. Stosując histogram liczby nadawanych imion spróbuj odpowiedzieć na pytanie co zmieniło się między rokiem 2000 a 2013 czy zmiana w trendzie wynika tylko z zmiany zwyczajów czy też innych czynników (czy potrafisz zidentyfikować te czynniki?)
    3. Przeanalizuj czy w Polsce również preferowane są imiona kończące się na określone litery (jak w USA). Wyznacz 3 litery, dla których zaobserwowano największą zmianę popularności między rokiem 2000 a 2024. Dla tych liter wyświetl przebieg trendu popularności w całym okresie czasu (dla każdego roku)
    

## *Uwagi:*
    - jako rozwiązanie prześlij skrypt - pojedynczy plik `py`. Pliki wejściowe (dane w zadaniu) powinny być zaczytywane ścieżką względną z podkatalogu `./data`. 
    - przed przesłanie rozwiązania proszę zweryfikować czy skrypt się uruchamia. (skrypty z błędami nie będą analizowane)
    - w komentarzach umieść informację o zadaniu, którego dotyczy dana część kodu
    - kody będą poddane analizie antyplagaitowej



---
Autorzy: *Piotr Kaczmarek* 
