# Lab 05 - Projekt podsumowujący biblioteki Pandas i Matplotlib

## Cel projektu
Celem projektu jest utrwalenie wiedzy dotyczącej pobierania i wczytywania danych oraz biblioteki Pandas.
W celu realizacji części zadań zapoznaj się z przykładami i informacjami dotyczącymi przetwarzania danych tabelarycznych w tym mechanizmu wieloindeksowania. W zadaniach wystarczające jest wykorzystanie metody tabeli przestawnej (`pivot_table`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html) lub/i metody grupowania (`groupby`). Przydatnymi metodami wykorzystywanymi w dalszej części zajęć będą też metoda dyskretyzacji `cut`, faktoryzacji (`factorize`), oraz wyznaczanie częstości wystąpień i normalizacji (`crosstab`)
Informacje na ten temat możesz znaleźć [tutaj](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html)

## Opis zadania
Na stronie Social Security Administration umieszczono dane zawierającą listę imion oraz częstotliwość ich występowania w latach 1880-2022. Pliki z danymi w formacie CSV dostępne są [tutaj](https://www.ssa.gov/oact/babynames/names.zip).

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
8. Wykreśl wykres z podziałem na lata i płeć zawierający informację jaki procent w danym roku stanowiły imiona należące do rankingu top1000 (wyznaczonego dla całego zbioru (pkt 6)). Wykres ten opisuje różnorodność imion, wyświetl rok, w którym zaobserwowano największą różnicę w różnorodności między imionami męskimi a żeńskimi .
9. Zweryfikuj hipotezę czy prawdą jest, że w obserwowanym okresie rozkład ostatnich liter imion męskich uległ istotnej zmianie? W tym celu 
    - dokonaj agregacji wszystkich urodzeń w pełnym zbiorze danych z podziałem na rok i płeć i ostatnią literę,
    - wyodrębnij dane dla lat 1917, 1967, 2022
    - znormalizuj dane względem całkowitej liczby urodzin w danym roku
    - wyświetl dane popularności litery dla mężczyzn w postaci wykresu słupkowego zawierającego poszczególne lata i gdzie słupki grupowane są wg litery. Wyświetl, dla której litery wystąpił największy wzrost/spadek między rokiem 1917 a 2022)
    - Dla 3 liter dla których zaobserwowano największą zmianę wyświetl przebieg trendu popularności w maksymalnym przedziale czasu
10.  Znajdź w rankingu top1000 imiona, które nadawane były zarówno dziewczynkom jak i chłopcom (stosunek nadanych imion męskich i żeńskich). Wyznacz 2 imiona, dla których zaobserwowano największą zmianę (definiowanej jako największa różnica stosunku imion męskich do żeńskich w badanych latach). Do analizy zmiany  wykorzystaj 2 przedziały: zagregowane dane do roku 1930 i od roku 2000. 
     - wyświetl te imiona
     - wkreśl przebieg trendu dla tych imion
<!-- 11. Spróbuj znaleźć najpopularniejsze imiona, które przez pewien czas były imionami żeńskimi/męskimi a następnie stały się imionami męskimi/żeńskimi.
    - możesz spróbować wyliczyć dla każdego imienia stosunek w którym nadawane było chłopcom i dziewczynkom
    - następnie oblicz zagregowaną wartość tego współczynnika w latach 1880-1920 oraz w okresie 2000-2020 i na tej podstawie wybrać imiona dla których zaobserwowana zmiana jest największa (zanotuj dwa najpopularniejsze imiona)
    - wkreśl przebieg trendu dla tych imion

    **Uwaga:** Do określenia popularności imienia możesz użyć danych z kolumn `frequency_male` i `frequency_female` i wyrażenia w postaci współczynnika: 
    <center>
     <img src="_images/lab_proj1/popularity.png" alt="drawing" height="50"/> 
    </center>
    Wtedy Jeśli dane imię występuje wyłącznie dla mężczyzn wartością wyrażenia będzie 1, jeśli tylko u kobiet 0. Przyjmij, że w rankingu zmiany imienia ze względu na płeć uwzględniane są tylko elementy, których początkowa i końcowa dysproporcja była mniejsza niż 70%. Np. w latach 1880-1920 wartość współczynnika wynosiła więcej niż 0.7 lub mniej niż 0.3 a następnie zmieniła się odpowiednio na wartość mniejszą niż 0.3 lub większą niż 0.7. Listę rankingową skonstruuj wybierając imiona wg popularności w rankingu 2000 najpolularniejszych imion (dla obu płci). -->

1.    Wczytaj dane z bazy opisującej dane demograficzne w okresie od 1935-2020r w poszczególnych grupach wiekowych W USA: [USA_demography](_resources/lab_04/demography_us_2023.sqlite3), opis: https://www.mortality.org/Data/ExplanatoryNotes ([wersja_pdf](_resources/lab_04/Explanatory Notes.pdf)). Spróbuj zagregować dane już na etapie zapytania SQL.  
2.   Wyznacz i wyświetl przyrost naturalny w każdym roku analizowanego okresu
3.   Wyznacz i wyświetl współczynnik przeżywalności dzieci w pierwszym roku życia ww każdym roku analizowanego okresu.
4.   Dokonaj porównania różnic w przyroście naturalnym bazującym na liczbie nadawanych imion dziewczynek i chłopców w danym roku z danymi dotyczącymi liczby urodzin z bazy danych 
    - przedstaw te różnice w formie graficznej (jako błąd względny w poszczególnych latach)
    - wyznacz i wyświetl informacje o roku w którym ten błąd był największy a w którym najmniejszy (węź pod uwagę wartość bezwzględną)
<!-- 15. Na wykresie z pkt 14 wyznacz współczynnik przeżywalności dzieci w pierwszych 5 latach życia (pamiętaj, że dla roku urodzenia x należy uwzględnić śmiertelność w grupie wiekowej 0 lat w roku x, 1rok w roku x+1 itd).
    
    **Uwaga**: Współczynnik przeżywalności w roku `y` może być wyznaczony na podstawie informacji o liczbie urodzin w danym roku `lu_y` oraz umieralności dzieci (`dx(k)_y+k`) w wieku `k` lat w roku `y+k`. Może być wyrażona wzorem:
<center>
     <img src="_images/lab_proj1/przezywalnosc.png" alt="drawing" height="50"/> 
    </center> -->
*Uwagi:*
- jako rozwiązanie prześlij skrypt - pojedynczy plik `py`. Pliki wejściowe (dane w zadaniu) powinny być zaczytywane ścieżką względną z podkatalogu `./data`. 
- przed przesłanie rozwiązania proszę zweryfikować czy skrypt się uruchamia. (skrypty z błędami nie będą analizowane)
- w komentarzach umieść informację o zadaniu, którego dotyczy dana część kodu
- kody będą poddane analizie antyplagaitowej



---
Autorzy: *Piotr Kaczmarek* 
