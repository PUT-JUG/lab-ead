# Lab 04 - Projekt podsumowujący biblioteki Pandas i Matplotlib

## Cel projektu
Celem projektu jest utrwalenie wiedzy dotyczącej pobierania i wczytywania danych oraz biblioteki Pandas.
W celu realizacji części zadań zapoznaj się z przykłądami i informacjami dotyczącymi przetwarzania danych tabelarycznych w tym mechanizmu wieloindeksowania. W zadaniach wystarczające jest wykorzystanie metody tabeli przestawnej (`pivot_table`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html) lub/i metody grupowania (`groupby`). Przydatnymi metodami wykorzystywanymi w dalszej części zajęć będą też metoda dyskretyzacji `cut`, faktoryzacji (`factorize`), oraz wyznaczanie częstości wystąpień i normalizacji (`crosstab`)
Informacje na ten temat możesz znaleźć [tutaj](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)

## Opis zadania
Na stronie Social Security Administration umieszczono dane zawierającą listę imion oraz częstotliwość ich występowania w latach 1880-2019. Pliki z danymi w formacie CSV dostępne są [tutaj](https://www.ssa.gov/oact/babynames/names.zip).

1. Wczytaj dane ze wszystkich plików do pojedynczej tablicy (używając Pandas).
2. Określi ile różnych (unikalnych) imion zostało nadanych w tym czasie.
3. Określi ile różnych (unikalnych) imion zostało nadanych w tym czasie rozróżniając imiona męskie i żeńskie.
4. Stwórz nowe kolumny `frequency_male` i `frequency_female` i określ popularność każdego z imion w danym każdym roku dzieląc liczbę razy, kiedy imię zostało nadane przez całkowita liczbę urodzeń dla danej płci.  
5. Określ i wyświetl wykres złożony z dwóch podwykresów, gdzie osią x jest skala czasu, a oś y reprezentuje:
   - liczbę urodzin w danym roku (wykres na górze)
   - stosunek liczby narodzin dziewczynek do liczby narodzin chłopców (wykres na dole)
W którym roku zanotowano najmniejszą, a w którym największą różnicę w liczbie urodzeń między chłopcami a dziewczynkami? 
5. Wyznacz 1000 najpopularniejszych imion dla każdej płci w całym zakresie czasowym, metoda powinna polegać na wyznaczeniu 1000 najpopularniejszych imion dla każdego roku i dla każdej płci a następnie ich zsumowaniu w celu ustalenia rankingu top 1000 dla każdej płci.
6. Wyświetl wykresy zmian dla imion *Harry* i *Marilin* oraz pierwszego imienia w żeńskiego i męskiego w rankingu:
    - na osi Y po lewej liczbę razy kiedy imę zostało nadane w każdym roku (zanotuj ile razy nadano to imię w 1940, 1980 i 2019r)?
    - na osi Y po prawej popularność tych imion w każdym z lat
7. Wykreśl wykres z podziałem na lata i płeć zawierający informację jaki procent w danym roku stanowiły imiona należące do rankingu top1000. Wykres ten opisuje różnorodność imion, zanotuj rok w którym zaobserwowano największą różnicę w różnorodności między imionami męskimi a żeńskimi.
8. Zweryfikuj hipotezę czy prawdą jest, że w obserwowanym okresie rozkład ostatnich liter imion męskich uległ istotnej zmianie? W tym celu 
    - dokonaj agregacji wszystkich urodzeń w pełnym zbiorze danych z podziałem na rok i płeć i ostatnią literę,
    - wyodrębnij dane dla lat 1910, 1960, 2015
    - znormalizuj dane względem całkowitej liczby urodzin w danym roku
    - wyświetl dane popularności litery dla każdej płci w postaci wykresu słupkowego zawierającego poszczególne lata i gdzie słupki grupowane są wg litery. Zanotuj, dla której litery wystąpił największy wzrost/spadek między rokiem 1910 a 2015)
    - Dla 3 liter dla których zaobserwowano największą zmianę wyświetl przebieg trendu popularności w czasie
9.  Znajdź imiona, które nadawane były zarówno dziewczynkom jak i chłopcom (zanotuj najpopularniejsze imię męskie i żeńskie)
10. Spróbuj znaleźć najpopularniejsze imiona, które przez pewien czas były imionami żeńskimi/męskimi a następnie stały się imionami męskimi/żeńskimi.
    - możesz spróbować wyliczyć dla każdego imienia stosunek w którym nadawane było chłopcom i dziewczynkom
    - następnie oblicz zagregowaną wartość tego współczynnika w latach 1880-1920 oraz w okresie 2000-2020 i na tej podstawie wybrać imiona dla których zaobserwowana zmiana jest największa (zanotuj dwa najpopularniejsze imiona)
    - wkreśl przebieg trendu dla tych imion
11. Wczytaj dane z bazy opisującej śmiertelność w okresie od 1959-2018r w poszczególnych grupach wiekowych: [USA_ltper_1x1.sqlite](_resources/lab_04/USA_ltper_1x1.sqlite) . Spróbuj zagregować dane już na etapie zapytania SQL.
12. Wyznacz przyrost naturalny w analizowanym okresie
13. Wyznacz i wyświetl współczynnik przeżywalności dzieci w pierwszym roku życia
14. Na wykresie z pkt 14 wyznacz współczynnik przeżywalności dzieci w pierwszych 5 latach życia (pamiętaj, że dla roku urodzenia x należy uwzględnić śmiertelność w grupie wiekowej 0 lat w roku x, 1rok w roku x+1 itd).

Jako rozwiązanie prześlij skrypt - pojedynczy plik `py`. Pliki wejściowe powinny być zaczytywane ścieżką względną bezpośrednio z katalogu roboczego.

---
Autorzy: *Piotr Kaczmarek*  i *Jakub Tomczyński*
