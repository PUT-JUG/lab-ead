# Lab 05 - Czyszczenie danych

Celem czyszczenia danych jest:
- wykrycie elementów brakujących i ich uzupełnienie lub usunięcie wierszy
- konwersja danych (np daty) i typów nominalnych (w tym korekta błędów w nazwach elementów, np. poznań, Poznan, Pznan, Poznań)
- analiza rozkładów i usunięcie elementów odstających (outlierów) (Lab 06)
- normalizacja danych i normalizacja rozkładu (Lab 06)

W zadaniu spróbuj odnieść efekty wprowadzonych zmian do efektu dla zadania klasyfikacji. Do oceny zastosuj funkcję:

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


def score_dataset(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)
```

Do oceny skuteczności klasyfikacji stosuj zawsze zbiór uczący i testowy, tzn. wszelkie hipotezy, wyznaczanie statystyk (np. wartości średniej, kwartyli) wyznaczaj wyłącznie dla zbioru uczącego, a następnie metodę zastosuj dla zbioru testowego (bez zmiany wartości wyznaczonych parametrów). Podział na zbiór uczący i testowego przeprowadź w proporcji 70/30%. Podział na zbiory przeprowadź na początku i potem używaj tych zbiorów dla wszystkich danych (rozwiązanie to zawiera pewien błąd metodyczny wynikający z wielokrotnego wykorzystania tego samego zbioru, zajmiemy się tym na Lab 07).

```python
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
1. Funkcja `score_dataset` zwraca średnią z wartości bezwzględnej błędu dla zbioru testowego. 
2. Do oceny skuteczności stosujemy zbiór testowy, który nie został użyty w procedurze uczenia i wyboru metody.
3. Pamiętaj jednak, że jednoznaczna interpretacja tego czy różnica między oboma podejściami jest istotna statystycznie wymaga rozszerzonej analizy, zajmiemy się tym na Lab 07.
4. Porównując otrzymany wynik błędu spróbuj określić dlaczego nastąpiła zmiana, pamiętaj przy tym, że podejście związane z czyszczeniem danych zależy od typu danych.  

## Elementy brakujące

1. Wczytaj zbiór danych z [pliku](./_resources/lab_05/melb_data.csv) do zmiennej `df`
2. Wyznacz liczbę wartości brakujących (pustych) i przeanalizuj w jakich kolumnach występują braki

```python
missing_values_count = df.isnull().sum()
```
- spróbuj określić dla każdej kolumny procent występowania wartości brakujących. Wyświetl je w postaci tabeli, gdzie indeksem jest nazwa kolumny, a kolumnami procent braków oraz całkowita liczba braków (możesz użyć metody `pd.concat`)

### Podejście 1: usunięcie kolumn/wierszy zawierających przynajmniej 1 element pusty - przetestuj oba podejścia:

```Python
df_cleaned_rows = df_set.dropna()
df_cleaned_cols = df_set.dropna(axis=1)
```
- Zastanów się, które z tych podejść powinno być zastosowane jeśli chcemy stworzyć klasyfikator predykujący ceny nieruchomości?
- Czy wiesz, które wiersze zostały usunięte? Spróbuj wyodrębnić listę ich indeksów.
- Sprawdź dokumentację [dropna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html) i zobacz:
  -  w jaki sposób usunąć tylko wiersze z jeśli wartości puste są w kolumnie `BuildingArea`, 
  -  ograniczając liczbę wierszy sprawdź ile zostanie wierszy jeśli usunie się wiersze, które nie mają **równocześnie** wypełnionego pola `BuildingArea` i  `YearBuilt`
  
### Podejście 2: wypełnienie pustych wartości np. zerami lub wartością, która poprzedza wartość brakującą
``` Python
df_cleaned_zeros = df.fillna(0) # wypełnia zerami
df_cleaned_bfill = df.fillna(method='bfill', axis=0).fillna(0)  # wypełnia wartością poprzedzającą z kdanej olumny, jeśli to niemożliwe, wstawia 0
```
- Zastanów się kiedy takie podejście może być stosowane, czy można je użyć do klasyfikacji?, sprawdź w dokumentacji [fillna](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html) jakie są jeszcze możliwości wypełnienia wypełnienia?
- kiedy wypełnianie wartością sąsiednią ma sens? Jeśli stosujemy je do klasyfikacji to jaką strategię przyjąć w odniesieniu do brakujących wartości referencyjnych (jest to wartość, która ma być predykowana przez klasyfikator) a jaką w odniesieniu do brakujących cech (wartość/wartości, które są wejściem klasyfikatora)?

### Podejście 3: podstawienie wartości średniej/mediany/mody:

``` Python
from sklearn.impute import SimpleImputer
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean') 
df_train_numeric = df_test.select_dtypes(include=[np.number]).copy()
df_test_numeric = df_test.select_dtypes(include=[np.number]).copy()#wybór tylko kolumn przechowujacych liczby, należy wykonać kopię obiektu
df_train_numeric.loc[:] = imp_mean.fit_transform(df_train_numeric)#dopasowanie parametrów (średnich) i transformacja zbioru uczącego

df_test_numeric[:]  = imp_mean.transform(df_test_numeric) #zastosowanie modelu do transformacji zbioru testowego (bez wyznaczania parametrów)
```
- kiedy wypełnianie wartością średnią/medianą ma sens? Jeśli stosujemy je do klasyfikacji to jaką strategię przyjąć w odniesieniu do brakujących wartości referencyjnych (jest to wartość, która ma być predykowana przez klasyfikator) a jaką w odniesieniu do brakujących cech (wartość/wartości, które są wejściem klasyfikatora)?
- oceń skuteczność klasyfikacji i porównaj ją z pozostałymi podejściami


## Konwersja danych

### konwersja daty
- konwersja danych z datą
- wyznaczanie interwałów
- wyznaczanie dnia tygodnia

### zmienne nominalne
- konwersja na zmienną nominalną
#### Łączenie zmiennych nominalnych (usuwanie literówek) przy pomocy fuzzywuzzy
Często dane wprowadzane w importowane dane zawierające teskty (słowa) traktowane jako zmienne nominalne, zawierają literówki, różnią się wielkością liter lub np. w przypadku nazw miejsc: posiadają lub nie dodatkowe człony (np. Ostrów i Ostrów Wlkp i Ostrow Wielkoposlki, jak również ostrow wlkp).
W przypadku zmiany różnicy w wielkości liter możliwe jest konwersja wszystkich elementów w kolumnie na np. małe litery oraz usunięcie znaków spacji. Sprawdź (używając `np.unique(...)`)ile różnych unikalnych elementów w kolumnie `Suburb`? Porównaj ten wynika z wynikiem otrzymanym po znormalizowaniu wielkości liter oraz usunięciu końcowych znaków spacji
```python
# zmiana na małe litery
df['Suburb']=df['Suburb'].str.lower()
# usunięcie końcowych spacji
df['Suburb'] = df['Suburb'].str.strip()
```
W danych mogą się jednak znajdować takie same elementy różniące się literą (literówka) lub posiadające dodatkowe człony w nazwie. Do porównania dwóch napisów, lub napisu z listą innych napisów można użyć moduł `fuzzywuzz`
```python
import fuzzywuzzy
fuzzywuzzy.process.extract('Ostrów',['ostrow', 'Ostrów Wlkp', 'ostrów wlkp', 'Ostrzeszów'])
```
Funkcja zwróci listę krotek, gdzie drugi element określa podobieństwo.
Do scalenia pewnego ciągu znaków z elementami kolumny pandas, może służyć funkcja:

```python
import fuzzywuzzy
def replace_matches_in_column(df, column, string_to_match, min_ratio = 90):
    # get a list of unique strings
    strings = df[column].unique()
    
    # get the top 10 closest matches to our input string
    matches = fuzzywuzzy.process.extract(string_to_match, strings, 
                                         limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

    # only get matches with a ratio > 90
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]

    # get the rows of all the close matches in our dataframe
    rows_with_matches = df[column].isin(close_matches)

    # replace all rows with close matches with the input matches 
    df.loc[rows_with_matches, column] = string_to_match
```
- spróbuj zastosować funkcję `replace_matches_in_column` do scalenia elementów w kolumnie `Suburb`, pamiętaj, że trzeba ją wywołać osobno dla każdego unikalnego elementu. Ile unikalnych elementów zostanie, jeśli minimalny próg podobieństwa ustalisz na wartość 90?
  
#### zmienna porządkowa -> konwersja na liczbę

``` Python
from sklearn.preprocessing import LabelEncoder

# Make copy to avoid changing original data 
label_train = train_df.copy()
label_test = test_df.copy()

# Apply label encoder to each column with categorical data
label_encoder = LabelEncoder()
col='CouncilArea'
label_train[col] = label_encoder.fit_transform(label_train[col])
label_test[col] = label_encoder.transform(label_test[col])

```
#### zmienna nominalna -> zastosowanie encodera
``` Python
from sklearn.preprocessing import LabelBinarizer

label_binarizer = LabelBinarizer()
lb_results = lb.fit_transform(cat_df_flights_onehot_sklearn['carrier'])
lb_results_df = pd.DataFrame(lb_results, columns=lb.classes_)
```



---
Autorzy: *Piotr Kaczmarek* i *Jakub Tomczyński*
