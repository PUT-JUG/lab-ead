# Lab 04 - Projekt podsumowujący zajęć dotyczących testowania hipotez

## Cel projektu
Celem projektu jest utrwalenie podsumowanie elementów związanych z testowaniem hipotez.
Przedmiotem projektu będzie zweryfikowanie hipotez dotyczących następujących związanych z COVID.

## Metryki i dane dla dalszej analizy
### Dane COVID-19
Informacje o covid pochodzą z 3 zbiorów danych utrzymywanych przez CSSE na Uniwersytecie Johna Hopkinsa: [repozytorium](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series).
Tabele zawierają następujące informacje:
- skumulowana liczba przypadków zachorowań dla poszczególnych krajów `time_series_covid19_confirmed_global.csv`
- skumulowana liczba zgonów dla poszczególnych krajów `time_series_covid19_deaths_global.csv`
- skumulowana liczba osób, które wyzdrowiały dla poszczególnych krajów `time_series_covid19_recovered_global.csv`

### Metryki COVID-19
1. Na podstawie danych wyznacz:
   - liczbę aktywnych przypadków (dla poszczególnych dni)
   - skumulowaną śmiertelność za każdy miesiąc, która określa liczbę zgonów do liczby osób, które wyzdrowiały w danym miesiącu
   - jeśli dany kraj nie publikuje wyników o liczbie osób, które wyzdrowiały przyjmij że czas trwania infekcji wynosi 14 dni
   - jeśli dany kraj nie publikuje wyników o śmiertelności usuń go z listy
   - w dalszej analizie nie uwzględniaj danych wyznaczonych dla mniej niż 100 aktywnych przypadków.
2. Ponieważ dane różnią się między sobą bezwzględna liczb a zachorowań, która zależy od wielu czynników np. gęstość zaludnienia, proponujemy, żeby testowanie hipotezy dotyczącej wpływu temperatury na rozwój wirusa testować na podstawie znormalizowanego współczynnika reprodukcji wirusa `R`. Jest kilka metod wyznaczania tego współczynnika, załóżmy jednak metodę bardo uproszczoną polegającą na porównaniu liczby zachorowań w okresach 1 tygodnia.
W celach pomocniczych wyznacz średnią liczbę infekcji za ostatnie 7 dni dla dnia `i`:

![mean_inf](./_images/lab_09/mean_infections.svg)

Współczynnik reprodukcji dla dnia `i` wyznacz jako:

![R_inf](./_images/lab_09/R_equation.svg)

gdzie wyrażenie uwzględnia że pierwsze objawy zakażenia występują po 5 dniach od wystąpienia kontaktu.

### Dane meteorologiczne
Dane meteorologiczne o minimalnej i maksymalnej temperaturze w danym miesiącu (dane z 2018r) dostępne są w pliku [TerraClimate_tmax_2018.nc](https://chmura.put.poznan.pl/s/8GI44MgN9zwRQAX)
[TerraClimate_tmin_2018.nc](https://chmura.put.poznan.pl/s/6PUjoY9LOx8VKL8)

Przykład importu pliku wygląda następująco:
``` python
import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
weather = Dataset('./data/TerraClimate_tmax_2018.nc')
month = 0 #styczeń
print(weather.variables.keys())
plt.imshow(weather['tmax'][month])
```
zmienna `weather` jest słownikiem, zawierającym klucze: `'lat', 'lon', 'time', 'crs', 'tmax', 'station_influence'`. gdzie `tmax` jest tablicą 3D, z pierwszą kolumną odpowiadającą miesiącowi (0-11), kolejne kolumny odpowiadają indeksowi szerokości i długości geograficznej, których wartości zawiera odpowiednio `weather['lat']`, `weather['lon']`.

Wyznacz wartość estymaty temperatury średniej wyrażonej jako średnia temperatur ekstremalnych.

## Testowanie hipotez
Dla zbioru danych sprawdź następujące hipotezy
1. Temperatura otoczenia istotnie wpływa na szybkość rozprzestrzeniania się wirusa. 
Załóż, że analizę prowadzimy dla zmiennych, którymi jest dyskretnych zakresów wartości temperatur średnich w miesiącu [<0; 0-10, 10-20, 20-30, 30>]. Natomiast analizowaną wartością jest  znormalizowaną wartość współczynnika reprodukcji wyznaczana oddzielnie dla każdego kraju/regionu (wartość wyznacz dzieląc wszystkie współczynniki reprodukcji przez wartość maksymalną zaobserwowaną dla danego kraju).  Jeśli otrzymasz istotne różnice, przeprowadź analizę post-hoc.

2. Zbadanie czy między poszczególnymi krajami w Europie istnieją istotne różnice w śmiertelności z powodu COVID-19. Analizę zrealizuj na 2 sposoby:
   - używając testu niezależności chi2, gdzie danymi będzie całkowita liczba zgonów do całkowitej liczby zakażeń 
   - używając testu ANOVA, gdzie zmienną jest kraj, natomiast wartościami obserwowanymi śmiertelność za poszczególne miesiące. 

Spróbuj zinterpretować różnice, które mogą się pojawić.


## Rozwiązanie

Jako rozwiązanie prześlij skrypt - pojedynczy plik `py`, realizujący poszczególne zadania, natomiast komentarz do wyniku umieść jako komentarz do skryptu. Pliki wejściowe powinny być zaczytywane ścieżką względną bezpośrednio z katalogu roboczego.

---
Autorzy: *Piotr Kaczmarek*  i *Jakub Tomczyński*
