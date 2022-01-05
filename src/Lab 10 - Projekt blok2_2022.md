# Lab 10 - Projekt podsumowujący zajęć dotyczących testowania hipotez

## Cel projektu
Celem projektu jest utrwalenie podsumowanie elementów związanych z testowaniem hipotez i eksploracją danych
Przedmiotem projektu będzie analiza danych dotyczących zużycia w latach 2004/5-2018 prądu w regionie miasta [Dayton](https://chmura.put.poznan.pl/s/aJ95P7abs9OANRK) oraz stanu [Virginia](https://chmura.put.poznan.pl/s/fIz5Ksytujup80b). Dodatkowo dla analizowanych obszarów będzie trzeba pozyskać dane o warunkach klimatycznych (z kilku dostępnych możliwości polecam np. [visualcrossing.com](https://www.visualcrossing.com/)])

## Informacje dotyczące opracowania i prezentacji danych
Ostateczny raport z analizy przedstaw w formie jupyter notebook, możesz jednak dołączyć dodatkowe pliki ze skryptami, z których korzysta notatnik. Jeśli Wykorzystujesz dane (np. informację o temperaturze) to należy je również załączyć. Jeśli do pozyskania danych wykorzystałeś własne skrypty to również powinny być dołączone z krótką informacją dotyczącą ich przeznaczenia.
Jeśli analizujesz istotność danego czynnika, istotność różnicy zużycia energii między dniami roboczymi a świątecznymi, czy poszukujesz anomalii w zużyciu energii pamiętaj o tym, że wnioski muszą opierać się na analizie przedziałów ufności (w przypadku czynników analizowanych przy pomocy regresji), lub wynikach testów statystycznych. Zastosowany sposób analizy powinien zostać krótko uzasadniony.

## Zadania
Temat projektu określa pewne ramy, które powinien objąć, pozostałe elementy proszę zrealizować w oparciu o dotychczas pozyskaną wiedzę oraz ew. dane które dostarczają informacji o innych potencjalnie ważnych czynnikach, które mogą mieć wpływ na zużycie energii (np. dni święta ruchome, nasłonecznienie, anomalie klimatyczne (np. huragany)).

W analizie danych poszukujemy czynników wpływających na zużycie energii tak, żeby po ich określeniu można było dokonać predykcji zużycia energii w pewnym horyzoncie czasu.

### faza I - analiza czynnikowa i eksploracja
W pierwszej fazie projektu proszę skupić się na wynikach dla miasta Dayton. 
W ramach projektu minimalne należy sprawdzić jak (i czy) następujące czynniki wpływają na zużycie energii:
1. temperatura dobowa
2. pora roku
3. pora dnia 
4. dni tygodnia i weekendy (możesz założyć dni pracujące/wolne od pracy)
5. czynniki globalne (np. wynikające ze zwiększania/zmniejszania liczby mieszkańców) - ten czynnik obserwowany jest jako pewien globalny trend/fluktuacje zużycia energii w okresie obserwacji
6. Na podstawie własnej analizy danych oraz informacji ogólnie dostępnych możesz zaproponować inne czynniki.  

Pamiętaj że analizując np. wpływ konsumpcji w określone dni tygodnia dane powinny zostać zagregowane (np. jedna skumulowana wartość/dzień), to samo dotyczy analizy ze względu na porę roku np. 1 wartość na tydzień - okno uśredniania dobierz kierując się swoją wiedzą i wstępną analizą. Pamiętaj że celem agregacji jest wyeliminowanie wpływu czynników zaburzających.

Do analizy  możesz wykorzystać np. korelację, regresję, możesz również spróbować zamodelować obserwowane zjawiska za pomocą funkcji analitycznej. Możesz założyć, że część czynników ma charakter ciągły a część może być traktowana jako zmienne nominalne. Sprawdź czy podane czynniki są wzajemnie zależne, i czy są addytywne?

Efektem prac powinno być stworzenie analitycznych modeli wykorzystujących istotne statystycznie czynniki i umożliwiających opis zużycia energii w porze dnia, w dniu tygodnia czy też w zależności od pory roku.

### faza  II - predykcja
W fazie tej należy wykorzystać modele opracowane w fazie I. Możesz również spróbować stworzyć model oparty np. o drzewa decyzyjne i porównać jego wyniki z wynikami otrzymanymi z analitycznego modelu fazy I.
- Zakładając, że znamy wyniki do końca roku 2017, spróbuj oszacować średnie zużycie energii w kolejnych tygodniach pierwszych 6 miesięcy roku 2018. Jeśli w zbudowanym modelu wykorzystujesz informację o temperaturze to możesz odczytać faktyczną temperaturę z analizowanych tygodni (tego czynnika nie predykujemy tylko go odczytujemy z dostępnych danych). Wyznacz i wyświetl jaki jest błąd oceń dopasowanie modelu do danych

- spróbuj zbudować model zużycia energii w dni robocze. Czy konsumpcja energii w tych dniach istotnie różni się od zużycia energii w dni wolne? Jeśli tak to spróbuj odnaleźć w zbiorze anomalie (dni poza weekendami,  w których zużycie energii jest poza zakresem ufności) - spróbuj określić co było powodem anomalii? Możesz również w analizie sprawdzić czy istnieje istotnie statystyczna różnica między zużyciem w soboty, niedziele i dni robocze.

- zakładając że znamy zużycie energii w dni poprzedzające dzień 14.12.2016, oraz 14.07.2017 spróbuj wykreślić predykowane zużycia energii (w zależności od pory dnia lub godziny) w 7 kolejnych dniach. 

**Pamiętaj**, że przed dokonaniem predykcji możesz wyznaczyć parametry modelu w oparciu o dane historyczne, długość okresu poprzedzającego, który wykorzystasz do wyznaczenia parametrów modelu zależy od Ciebie, powinna jednak być uzasadniona.

### faza III 
Opracowany model spróbuj zastosować do danych z obszaru stanu Virginia. Wskaż czynniki, których wpływ jest istotnie (statystycznie) różny względem miasta Dayton. Ponieważ dane pochodzą z obszarów o różnym zaludnieniu, warto najpierw przeskalować dane z stanu Virginia, tak, żeby dopasować wartości absolutne do danych z Dayton, wyznaczenie współczynnika skalującego pozwoli na łatwiejszą analizę innych czynników (inaczej zawsze będziemy obserwowali istotną różnice)



--
Autorzy: *Piotr Kaczmarek* 
