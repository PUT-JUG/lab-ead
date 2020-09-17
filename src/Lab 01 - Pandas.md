# Lab 01 - wczytywanie i modyfikacja danych w *pandas*

W obrębie całego kursu do przechowywania i manipulacji danymi będziemy wykorzystywać narzędzia dostarczane przez bibliotekę `pandas`. Dla przypomnienia: *pandas* to biblioteka służąca do zarządzania i przetwarzania danych tabelarycznych. Pozwala na tworzenie dwuwymiarowych tabel z danymi wraz z nagłówkami i wygodną manipulację nimi: m.in. wycinanie określonych fragmentów, sklejanie wielu zestawów danych, interpolację czy import/eksport do wielu formatów plików. Biblioteka jest mocno powiązana z *NumPy*, chociaż przechowywane dane nie muszą być liczbami.

Stwórz projekt w PyCharm, utwórz nowy skrypt, w którym będziesz testować poznawane narzędzia. Zaimportuj bibliotekę `pandas` jako `pd` oraz `numpy` jako `np`. W przypadku tych biblbiotek zawsze trzymaj się tej konwencji importu.

## Klasa `DataFrame`

Podstawową klasą przechowującą dane jest `pd.DataFrame`. Dane mają układ dwuwymiarowej tabeli, kolumny mogą mieć *nagłówki*, a wiersze *indeks*. Stwórzmy przykładowy `DataFrame` przechowujący losowe dane o pogodzie poprzez przekazanie macierzy numpy jako *danych*, listy napisów jako *nagłówków kolumn* oraz wygenerowanego zakresu dat jako *indeksu wierszy*.

```python
num_days = 20
temperature = np.random.uniform(20, 28, size=(num_days, 1))
pressure = np.random.uniform(990, 1010, size=(num_days, 1))
rain = np.random.uniform(0, 20, size=(num_days, 1))
random_data = np.hstack((temperature, pressure, rain))
df_weather = pd.DataFrame(index=pd.date_range("20200501", periods=num_days, freq="1D"),
                          data=random_data, columns=["Temperature", "Pressure", "Rain"])

print(df_weather)
```

Przekazanie `DataFrame` do funkcji `print()` wyświetli zawartość tabeli (jeśli wierszy/kolumn jest dużo, zostaną wyświetlone tylko początkowe/końcowe):

```python
print(df_weather)
```

Możliwe jest też tworzenie `DataFrame` na bazie słownika, którego *klucze* zostaną potraktowane jako nagłówki kolumn, a *wartości* jako dane w danej kolumnie:

```python
df_people = pd.DataFrame({"Height": [180, 160, 195],
                          "Weight": [77, 52, 200]})
print(df_people)
```

Zauważ, że domyślne indeksy przyjmują wartości całkowite od 0 w górę.

### Podgląd `DataFrame` w interfejsie graficznym - `pandasgui`

W większości przypadków w zupełności wystarczy nam podgląd danych bezpośrednio w konsoli lub w komórce Jupytera, czasem jednak wygodniej jest przejrzeć dane w trybie okienkowym.

Zainstaluj pakiet `pandasgui` i zaimportuj go do skryptu. Przykladowe użycie w trybie blokującym (wykonywanie programu zostanie wstrzymane do czasu zamknięcia okna):

```python
pandasgui.show(df, settings={'block': True})
```

---

### Dostęp do danych, indeksowanie

Stwórzmy niewielki `DataFrame` do testów:

```python
vals = np.random.randn(6, 4)
df = pd.DataFrame(vals, index=[0.0, 0.2, 0.3, 0.7, 1.0, 1.3], columns=["A", "B", "C", "D"])
df
```

Dostęp do indeksów obiektu `DataFrame` możliwy jest przez właściwość `index`:

```python
df.index
```

Dostęp do zbioru kolumn poprzez właściwość `columns`:

```python
df.columns
```

Obie te metody zwracają specjalny obiekt `Index`, w zależności od typu. Możliwa jest łatwa konwersja na Pythonową listę:

```python
list_of_columns = list(df.columns)
for c in list_of_columns:
    print(c)
```

Korzystając z właściwości `values` uzyskamy dostęp do danych w przechowywanych tabeli w postaci macierzy NumPy:

```python
df.values
```

#### Indeksowanie

Główną przewagą przechowywania danych w postaci `DataFrame` w stosunku do zwykłej tablicy dwuwymiarowej/macierzy jest możliwość dostępu do danych po przydzielonych etykietach kolumn/wieszy. Poniższe metody zwracają nowy `DataFrame` będący fragmentem oryginalnego, obiekt `Series` (w przypadku pojedynczych wierszy lub kolumn) lub pojedynczy skalar.

Możliwe jest proste wybranie jednej lub kilku kolumn operatorem `[]`:

```python
df["B"]
```

```python
df[["C", "D"]]
```

Lub wierszy:

```python
df[0.2:1.0]
```

Dla uniknięcia możliwych pomyłek (w powyższych przykładach nie widać jednoznacznie czy wybór odbywa się po kolumnach czy po wierszach) zaleca się korzystanie z metod `loc[]` oraz `iloc[]`:

##### Indeksowanie po etykietach (loc)

Metoda `loc[]` pozwala wybrać fragment `DataFrame` korzystając z **etykiet**:

Wybór wiersza o etykiecie (indeksie) 0.7:

```python
df.loc[0.7, :]
```

Wybór kolumn o etykietach "A" oraz "B" (lista etykiet):

```python
df.loc[:, ["A", "B"]]
```

Możliwe jest podawanie również przedziałów i jednoczesny wybór po kolumnach i wierszach:

```python
df.loc[0.2:0.3, "A":"C"]
```

Wybór pojedynczej wartości (skalar):

```python
df.loc[0.2, ["B"]]
```

##### Indeksowanie po pozycjach (iloc)

Metoda `iloc[]` pozwala wybrać fragment `DataFrame` korzystając z **pozycji** opisanych liczbami całkowitymi - na identycznych zasadach jak w przypadku list czy macierzy NumPy:

Pojedyncze pozycje:

```python
df.iloc[2, 3]
```

Zakresy pozycji:

```python
df.iloc[3:5, 0:2] # wiersze 3,4; kolumny 0,1
```

Listy pozycji:

```python
df.iloc[[1, 2, 4], :] # wiersze 1,2,4, wszystkie kolumny
```

##### Wybór kolumn za pomocą wyrażenia regularnego

Metoda `filter()` pozwala na wybór kolumn (lub wierszy po podaniu opcjonalnego parametru `axis`) po etykietach, np. za pomocą dopasowania wyrażeniem regularnym:

```python
df.filter(regex=r"[A-C]")
```

##### Indeksowanie logiczne

Indeksowanie logiczne pozwala w bardzo szybki sposób wybrać fragmenty tabeli, które spełniają określony warunek. Przykładowo:

```python
df.loc[df["A"] > 0, :] # wybierz wszystkie wiersze, gdzie "A" jest większe od 0
```

Możliwe jest też budowanie bardziej złożonych warunków, na przykład:

```python
df.loc[(df["A"] > -0.75) & (df["B"] < 0.25), :]
```

##### Modyfikacja zawartości

Po wyborze fragmentu `DataFrame` możliwe jest przypisanie nowych wartości wybranej części operatorem przypisania `=`.

Przygotujmy nowy zbiór danych:

```python
alpha = np.array([0, np.pi/4, np.pi/2, np.pi*3/4, np.pi])

trig = pd.DataFrame({"sinus": np.round(np.sin(alpha), 10),
                     "cosinus" : np.round(np.cos(alpha), 10),
                     "x^2" : alpha**2,
                     "random" : np.random.randn(len(alpha))}, index=alpha)
```

Możliwe jest przypisanie skalara - wartość zostanie wpisana pod wszystkie pasujące elementy:

```python
trig.loc[1:4, "random"] = 0
```

Lub zbioru nowych wartości, na przykład w postaci macierzy NumPy, przy czym należy pamiętać o podaniu macierzy o odpowiednim rozmiarze:

```python
trig.loc[trig["cosinus"] >= 0, "random"] = np.array([1, 3, 5])
```

##### Dodawanie kolumn

Najprostszym sposobem na dodanie kolumny do struktury `DataFrame` jest przypisanie wartości do nieistniejącej kolumny, przykładowo:

```python
trig["New column"] = -1
```


TODO: zmiany nazw kolumn
zmiana indeksu


TODO zadanie

TODO wczytywanie, zapis do pliku

---


---
Autorzy: *Jakub Tomczyński*
