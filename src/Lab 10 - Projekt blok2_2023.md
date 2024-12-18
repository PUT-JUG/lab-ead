# Lab 10 - Projekt podsumowujący zajęć dotyczących testowania hipotez

## Cel projektu

Celem projektu jest utrwalenie podsumowanie elementów związanych z testowaniem hipotez i eksploracją danych
Przedmiotem projektu będzie analiza danych dotyczących sprzedaży jednej z dużych sieci handlowych.

[Dane](https://chmura.put.poznan.pl/f/31294188) pochodzą z ponad 1000 punktów sprzedaży i zostały zarejestrowane w czasie 1,5roku .

Dane zawierają (poniżej wymieniono pliki oraz kolumny, których nazwa nie jest oczywista):

`store_data.csv` - informacje na temat sprzedaży poszczególnych sklepów w obserwowanym okresie

- **Sales** - obrót handlowy w danym dniu (to jest to, co prognozujesz)
- **Customers** - liczba klientów w danym dniu
- **Open** - wskaźnik, czy sklep był otwarty: 0 = zamknięty, 1 = otwarty
- **StateHoliday** - wskazuje świąteczny dzień państwowy. Zazwyczaj wszystkie sklepy, z niewielkimi wyjątkami, są zamknięte w dniach świątecznych. Zauważ, że wszystkie szkoły są zamknięte w dni świąteczne i weekendy. a = dzień państwowy, b = święta wielkanocne, c = Boże Narodzenie, 0 = brak
- **SchoolHoliday** - wskazuje, czy (Sklep, Data) był dotknięty zamknięciem szkół publicznych
- **Promo** - wskazuje, czy sklep prowadzi promocję w danym dniu

`store.csv` - informacja dotycząca poszczególnych sklepów

  - **StoreType** - różnicuje między 4 różnymi modelami sklepów: a, b, c, d
  - **Assortment** - opisuje poziom asortymentu: a = podstawowy, b = dodatkowy, c = rozszerzony
  - **CompetitionDistance** - odległość w metrach do najbliższego konkurencyjnego sklepu
  - **CompetitionOpenSince[Month/Year]** - podaje przybliżony rok i miesiąc otwarcia najbliższego konkurenta
  - **Promo2** - Promo2 to kontynuowana i kolejna promocja w niektórych sklepach: 0 = sklep nie bierze udziału, 1 = sklep bierze udział
  - **Promo2Since[Year/Week]** - opisuje rok i numer tygodnia kalendarzowego, kiedy sklep zaczął uczestniczyć w Promo2
  - **PromoInterval** - opisuje ko- **StoreType** - różnicuje między 4 różnymi modelami sklepów: a, b, c, d
  - **Assortment** - opisuje poziom asortymentu: a = podstawowy, b = dodatkowy, c = rozszerzony
  - **CompetitionDistance** - odległość w metrach do najbliższego konkurencyjnego sklepu
  - **CompetitionOpenSince[Month/Year]** - podaje przybliżony rok i miesiąc otwarcia najbliższego konkurenta
  - **Promo2** - Promo2 to kontynuowana i kolejna promocja w niektórych sklepach: 0 = sklep nie bierze udziału, 1 = sklep bierze udział
  - **Promo2Since[Year/Week]** - opisuje rok i numer tygodnia kalendarzowego, kiedy sklep zaczął uczestniczyć w Promo2
  - **PromoInterval** - opisuje kolejne interwały, w których zaczyna się Promo2, wymieniając miesiące, w których promocja rozpoczyna się na nowo. Na przykład "Lut, Maj, Sie, Lis" oznacza, że każda runda zaczyna się w lutym, maju, sierpniu, listopadzie danego roku dla danego sklepu

`store_states.csv` - informacja o lokalizacji sklepu na terenie landu

`state_names.csv` - lista landów i ich skrótów

`weather.csv` - pogoda w poszczególnych landach i poszczególnych dniach, 


## Informacje dotyczące opracowania i prezentacji danych

Ostateczny raport z analizy przedstaw w formie jupyter notebook, możesz jednak dołączyć dodatkowe pliki ze skryptami, z których korzysta notatnik (przy założeniu że znajdują się one w tym samym katalogu co notatnik). Jeśli wykorzystujesz dodatkowe dane, które nie zostały załączone do datasetu to należy je również załączyć (gdy dane są wczytywane w notatniku powinny być zaczytywane z tego samego katalogu w którym znajduje się notatnik). Jeśli do pozyskania/przetworzenia danych z których później korzystasz w notatniku wykorzystałeś własne skrypty to również powinny być dołączone z krótką informacją dotyczącą ich przeznaczenia.
Jeśli analizujesz istotność danego czynnika, np. istotność zmiany sprzedaży podczas promocji, zmian temperatury lub cech sklepu, czy poszukujesz anomalii sprzedażowych to pamiętaj o tym, że wnioski muszą opierać się na analizie przedziałów ufności (w przypadku czynników analizowanych przy pomocy regresji), lub wynikach testów statystycznych. Zastosowany sposób analizy powinien zostać krótko uzasadniony.

## Zadania

Temat projektu określa pewne ramy, które powinien objąć, szczegółowe rozwiązania proszę zrealizować w oparciu o dotychczas pozyskaną wiedzę, własną widzę dziedzinową oraz ew. dodatkowe dane, które dostarczają informacji o innych potencjalnie ważnych czynnikach, które mogą mieć wpływ sprzedaż.

W analizie danych poszukujemy czynników wpływających na sprzedaż, tak, żeby po ich określeniu można było dokonać predykcji sprzedaży w pewnym horyzoncie czasu oraz zrozumieć relację między czynnikiem a wielkością sprzedaży.

### Faza I - analiza czynnikowa i eksploracja

W ramach projektu minimalne należy sprawdzić jak (i czy) następujące czynniki wpływają sprzedaż oraz spróbować wyjaśnić następujące kwestie:

Czynniki wpływające na sprzedaż oraz na liczbę odwiedzających i wartość koszyka

1. Typ sklepu
2. Dni wolne od nauki szkolnej
3. trwanie promocji
4. Dni tygodnia (pracujące) i weekendy
5. Dni miesiąca, możesz podzielić miesiąc na 3 części (po 10 dni) lub na tygodnie (po 7 dni) i sprawdzić czy sprzedaż w tych okresach się istotnie zmienia.
6. Pogoda (opady deszczu/śniegu)
7. Pora roku lub miesiąc
8. Na podstawie własnej analizy danych oraz informacji ogólnie dostępnych możesz zaproponować inne czynniki.


W analize w/w czynników prócz analizy globalnego wpływu na wszystkie dla całej populacji, spróbuj również ocenić czy istnieją istotne różnice między landami jeśli chodzi o wpływ  najważniejszych czynników (wytypuj własne  hipotezy na podstawie własnej analizy i wybierz 3 najbardziej prawdopodobne czynniki do analizy uwzględniającej specyfikę geograficzną)? Możesz np. sprawdzić czy pora roku (lub miesiąc) ma istotny  wpływ na zmianę sprzedaży pomiędzy landami np. tymi znajdującymi się an morzem czy w górach.

Wpływ analizowanych czynników oceniaj stosując metody statystyczne:

- dla czynników analizowanych za pomocą regresji możesz wykorzystać dane generowane z modelu ols
- dla czynników  (np. obecność promocji) wykorzystaj testy A/B


Spróbuj zaproponować sposób analizy, który pozwoli stwierdzić co mogą oznaczać typy sklepów a,b,c,d. Analizę oprzyj na analizie różnic między nimi (np. dotyczącej czasu pracy, obrotu, liczby klientów)

**Sugestie**

Do analizy  możesz wykorzystać np. korelację, regresję, możesz również spróbować zamodelować obserwowane zjawiska za pomocą funkcji analitycznej. Możesz założyć, że część czynników ma charakter ciągły a część może być traktowana jako zmienne nominalne. Sprawdź czy podane czynniki są wzajemnie zależne, i czy są addytywne?

Możesz próbować również, stosujące metody uczenia nienadzorowanego ocenić czy możemy, analizując dane z tabeli `store_data.csv` znaleźć pewne grupy (skupienia) sklepów i czy te skupienia są zależne np. od kategorii, asortymentu lub landu.

Efektem prac powinno być stworzenie analitycznych modeli wykorzystujących istotne statystycznie czynniki i umożliwiających opis wartości sprzedaży i liczby klientów   dla najbardziej istotnych czynników (np. opisujących zależność dla dnia tygodnia czy też pory roku czy pogody).

Uwaga: warto rozpocząć analizę czynnikową od czynników globalnych, wpływających w długim horyzoncie czasu (danych zawartych w `store.csv`) i po ich skompensowaniu analizować czynniki w coraz krótszym okresie czasu lub lokalizacji geograficznej. Np. w poszczególnych miesiącach, a po ich kompensowaniu analizować wpływ w poszczególnych dniach (np. wpływ opadów deszczu)

### Faza  II - predykcja

W fazie tej należy wykorzystać modele opracowane w fazie I. Możesz również spróbować stworzyć model oparty np. o drzewa decyzyjne i porównać jego wyniki z wynikami otrzymanymi z analitycznego modelu fazy I.

- spróbuj zbudować model sprzedaży dla poszczególnych dni. Czy wartość sprzedaży w dni robocze istotnie różni się od sprzedaży w dni wolne? Jeśli tak to spróbuj odnaleźć w zbiorze anomalie (dni poza daniami wolnymi i weekendami),  w których sprzedaż jest poza zakresem ufności - spróbuj określić co było powodem anomalii? Pamiętaj, że model sprzedaży w poszczególne dni powinien zostać odsprzężony od czynników sezonowych i innych czynników globalnych. (Z analizy fazy I powinieneś wiedzieć czy te czynniki działają w sposób addytywny czy multiplikatywny).
- Zakładając, że znamy wyniki do końca maja 2015, spróbuj oszacować średnią sprzedaż w kolejnych 8 tygodniach czerwca i lipca. Jeśli w zbudowanym modelu wykorzystujesz informację o temperaturze lub opadach to możesz odczytać faktyczne wartości z dostępnych danych (tego czynnika nie predykujemy tylko go odczytujemy z dostępnych danych). To samo dotyczy promocji.  Wyznacz i wyświetl jaki jest błąd dopasowania modelu do danych


**Pamiętaj**, że przed dokonaniem predykcji możesz wyznaczyć parametry modelu w oparciu o dane historyczne, długość okresu poprzedzającego, który wykorzystasz do wyznaczenia parametrów modelu zależy od Ciebie, powinna jednak być uzasadniona.

--
Autorzy: *Piotr Kaczmarek*
