# Lab 06 - Analiza danych i usuwanie outlierów
<!-- <-- https://www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python> -->
Celem czyszczenia danych jest:
- wykrycie elementów brakujących i ich uzupełnienie lub usunięcie wierszy
- konwersja danych (np daty) i typów nominalnych (w tym korekta błędów w nazwach elementów np. poznań, Poznan, Pznan, Poznań)
- analiza rozkładów i usunięcie elementów odstających (outlierów)
- normalizacja danych i normalizacja rozkładu

## Graficzna analiza rozkładu
1. Wczytaj zbiór danych z [pliku](./_resources/lab_05/melb_data.csv) do zmiennej ``df`` i używając funkcji ``stats.probplot``

2. heatmapa korelacji
3. Analiza współzależności 2 zmiennych
## Elementy brakujące
### Analiza wartości 0
Traktowanie wartości '0' jako brakującej.
   - Ile jest elementów, które mają cenę sprzedaży równą 0?
   - Przeanalizuje przykładowe wiersze i zastanów się z czego to wynika
   - Dla elementów z ceną '0' Wyświetl wykres `scatter` i przeanalizuje czy istnieje korelacja między tymi elementami 
   - czy ich usunięcie wpłynie na poprawę jakości klasyfikacji?
```Python
import seaborn as sns
sns.set()

sns.pairplot(land_0, height = 2.5)
plt.show();
```


### Usunięcie elementów odstających
1. Boxplot
2. IRQ
3. t-distribution

## Normalizacja rozkładu

## Wyznacza
---

#### 🔥 Zadanie 1 🔥

---
Autorzy: *Piotr Kaczmarek* i *Jakub Tomczyński*