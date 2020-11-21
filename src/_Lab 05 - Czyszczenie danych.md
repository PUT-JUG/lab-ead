# Lab 05 - Czyszczenie danych

Celem czyszczenia danych jest:
- wykrycie elementów brakujących i ich uzupełnienie lub usunięcie wierszy
- konwersja danych (np daty) i typów nominalnych (w tym korekta błędów w nazwach elementów np. poznań, Poznan, Pznan, Poznań)
- analiza rozkładów i usunięcie elementów odstających (outlierów) (Lab 06)
- normalizacja danych i normalizacja rozkładu (Lab 06)

W zadaniu spróbuj odnieść efekty wprowadzonych zmian do efektu dla zadania klasyfikacji. Do oceny zastosuj funkcję:
```Python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
def score_dataset(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)
```
Do oceny skuteczności stosuj zawsze zbiór uczący i tetsowy, tzn. wszelkie hipotezy, wyznaczanie statystyk (np. wartości średniej, kwartyli) wyznaczaj wyłącznie dla zbioru uczącego, a następnie metodę zastosuj dla zbioru testowego (bez zmiany wartości wyznaczonych parametrów). Podział na zbiór uczący i testowego przeprowadź w proporcji 70/30%. Podział na zbiory przeprowadź na początku i potem używaj tych zbiorów dla wszystkich danych (rozwiązanie to zawiera pewien błąd metodyczny wynikający z wielokrotnego wykorzystania tego samego zbioru, zajmiemy się tym na Lab 07)
```Python
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
train_df,test_df = train_test_split(df, test_size=0.7)
#czyszczenie danych
#train_df_cleaned = ...
#test_df_cleaned = ...
cols_x = train_df_cleaned.columns.select_dtypes(include=[np.number]).difference(['Price']) #wybiera tylko kolumny z wartosciami numerycznymi,za wyjątkiem kolumny z wartością referencyjną
cols_y = 'Price'
print(score_dataset(train_df_cleaned[cols_x],test_df_cleaned[cols_x], train_df_cleaned[cols_y], test_df_cleaned[cols_y]))

```


**UWAGA** 
1. Funkcja ``score_dataset`` zwraca średnią z wartości bezwzględnej błędu dla zbioru testowy, 
2. Do oceny skuteczności stosujemy zbiór testowy, który nie został użyty w procedurze uczenia i wyboru metody
3. Pamiętaj jednak że jednoznaczna interpretacja tego czy różnica między oboma podejściami jest istotna statystycznie wymaga rozszerzonej analizy, zajmiemy się tym na Lab07.
4. Porównując otrzymany wynik błędu spróbuj określić dlaczego nastąpiła zmiana, pamiętaj przy tym że podejście związane z czyszczeniem danych zależy od danych.  

## Elementy brakujące
1. Wczytaj zbiór danych z [pliku](./_resources/lab_05/melb_data.csv) do zmiennej ``df``
2. Wyznaczanie liczbę wartości brakujących (pustych) i przeanalizuj w jakich kolumnach występują braki
```Python
missing_values_count = df.isnull().sum()
```
- spróbuj określić dla każdej kolumny procent występowania wartości brakujących. Wyświetl je w postaci tabeli gdzie indeksem jest nazwa kolumny a kolumnami procent braków oraz całkowita liczba braków (możesz użyć metody ``pd.concat``)
1. Podejście 1: usunięcie kolumn/wierszy zawierających przynajmniej 1 element pusty - przetestuj oba podejścia:
```Python
df_cleaned_rows = df_set.dropna()
df_cleaned_cols = df_set.dropna(axis=1)
```
- Zastanów się które z tych podejść powinno być zastosowane jeśli chcemy stworzyć klasyfikator predykujący ceny nieruchomości?
- czy wiesz które wiersze zostały usunięte - spróbuj wyodrębnić listę ich indeksów?
- sprawdź dokumentację [dropna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html) i zobacz:
  -  w jaki sposób usunąć tylko wiersze z jeśli wartości puste są w kolumnie ``BuildingArea``, 
  -  ograniczając liczbę wierszy sprawdź ile zostanie wierszy jeśli usunie się wiersze, które nie mają równocześnie wypełnionego pola ``BuildingArea`` i  ``YearBuilt``
4. Podejście 2: wypełnienie pustych wartości np. zerami lub wartością która poprzedza wartość brakującą
``` Python
df_cleaned_zeros = df.fillna(0) # wypełnia zerami
df_cleaned_bfill = df.fillna(method='bfill', axis=0).fillna(0) #wypełnia wartością poprzedzającą z kolumny, jeśli to niemożliwe, wstawia 0
```
- Zastanów się kiedy takie podejście może być stosowane, czy można je użyć do klasyfikacji?, sprawdź w dokumentacji [fillna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html) jakie są jeszcze możliwości wypełnienia wypełnienia?


5. Podejście 3: podstawienie wartości średniej/mediany/mody:
``` Python
from sklearn.impute import SimpleImputer
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean') 
df_train_numeric = df_test.select_dtypes(include=[np.number]).copy()
df_test_numeric = df_test.select_dtypes(include=[np.number]).copy()#wybór tylko kolumn przechowujacych liczby, należy wykonać kopię obiektu
df_train_numeric.loc[:] = imp_mean.fit_transform(df_train_numeric)#dopasowanie parametrów (średnich) i transformacja zbioru uczącego

df_test_numeric[:]  = imp_mean.transform(df_test_numeric) #zastosowanie modelu do transformacji zbioru testowego (bez wyznaczania parametrów)
```
- kiedy wypełnianie wartością sąsiednią ma sens? Jeśli stosujemy je do klasyfikacji to jaką strategię przyjąć w odniesieniu do brakujących wartości referencyjnych (jest to wartość, która ma być predykowana przez klasyfikator) a jaką w odniesieniu do brakujących cech (wartość/wartości, które są wejściem klasyfikatora)?
- oceń skuteczność klasyfikacji i porównaj ją z pozostałymi podejściami


## Konwersja danych
### konwersja daty
- konwersja danych z datą
- wyznaczanie interwałów
- wyznaczanie dnia tygodnia

### zmienne nominalne
- konwersja na zmienną nominalną
- Łączenie zmiennych nominalnych (usuwanie literówek)
- zmienna porządkowa -> konwersja na liczbę
- zmienna nominalna -> zastosowanie encodera


---

#### 🔥 Zadanie 1 🔥



---
Autorzy: *Piotr Kaczmarek* i *Jakub Tomczyński*
