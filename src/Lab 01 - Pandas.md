# Lab 01 - wstęp do *pandas*

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

Możliwe jest uzyskanie krótkiego podsumowania statystycznego tabeli metodą `describe()` (zwracany jest nowy `DataFrame` zawierający statystykę poszczególnych kolumn), a także podgląd początku (`head()`) i końca (`tail()`) tabeli.

```python
df_weather_summary = df_weather.describe()

print(df_weather_summary)
```

### Wyświetlanie danych na wykresie

Biblioteka pandas bardzo dobrze współpracuje z biblioteką do wyświetlania wykresów. Zaimportujmy `matplotlib.pyplot` jako `plt`, a następnie wywołajmy polecenia:

```python
df_weather.plot()
plt.show()
```

Pandas automatycznie ustawi etykiety osi oraz wypełni legendę nagłówkami kolumn, a osią *x* będzie indeks wierszy.

Możemy również wykorzystać wykresy punktowe (`kind=scatter`), słupkowe (`kind=bar`) lub ręcznie podać kolumny dla osi:

```python
df_weather.plot(kind='scatter', x='Temperature', y='Rain')
plt.show()
```

Do zaawansowanego wyświetlania danych na wykresach powrócimy w kolejnych laboratoriach.

### Podgląd `DataFrame` w interfejsie graficznym - `pandasgui`

W większości przypadków w zupełności wystarczy nam podgląd danych bezpośrednio w konsoli lub w komórce Jupytera, czasem jednak wygodniej jest przejrzeć dane w trybie okienkowym.

Zainstaluj pakiet `pandasgui` i zaimportuj go do skryptu. Przykladowe użycie w trybie blokującym (wykonywanie programu zostanie wstrzymane do czasu zamknięcia okna):

```python
pandasgui.show(df_weather, settings={'block': True})
```

---

### Dostęp do danych, indeksowanie

Stwórzmy niewielki `DataFrame` do testów:

```python
vals = np.random.randn(6, 4)
df = pd.DataFrame(vals, index=[0.0, 0.2, 0.3, 0.7, 1.0, 1.3], columns=["A", "B", "C", "D"])
print(df)
```

Dostęp do indeksów obiektu `DataFrame` możliwy jest przez właściwość `index`:

```python
print(df.index)
```

Dostęp do zbioru kolumn poprzez właściwość `columns`:

```python
print(df.columns)
```

Obie te metody zwracają specjalny obiekt `*Index`, w zależności od typu. Możliwa jest łatwa konwersja na Pythonową listę:

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

Główną przewagą przechowywania danych w postaci `DataFrame` w stosunku do zwykłej tablicy dwuwymiarowej/macierzy jest możliwość dostępu do danych po przydzielonych etykietach kolumn/wieszy. Poniższe operatory w zależności od sytuacji zwracają nowy `DataFrame` będący fragmentem oryginalnego, obiekt `Series` (w przypadku pojedynczych wierszy lub kolumn) lub pojedynczy skalar.

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

Wybieranie co n-tego wiersza:

```python
df.iloc[0::2, :] # co drugi wiersz, zaczynając od zerowego
```

##### Indeksowanie mieszanie ("`loc` + `iloc`")

Aby posługiwać się jednocześnie etykietami oraz indeksami porządkowymi (np. nazwami kolumn i numerami wierszy) najlepiej skonwertować etykiety na indeksy porządkowe i przekazać je do metody `iloc`. Przykładowo, jeśli chcemy wybrać wiersze od 0 do 2 włącznie, z kolumny `C`:

```python
df.iloc[0:3, df.columns.get_loc('C')]
```

---

**Uwaga!**

Pojedyncze indeksowanie za pomocą `loc` lub `iloc` zwraca *widok* na oryginalny `DataFrame`, co oznacza, że jeśli zmodyfikujemy znajdujące się w nim dane, zostaną one zmodyfikowane również w oryginalnym obiekcie. W przypadku złożonych indeksowań (np. `df.iloc[1:5, ].loc[: 'A']`) nie ma takiej gwarancji i w konsoli zostanie wydrukowane związane z tym ostrzeżenie.

---

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

#### Modyfikacja zawartości

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

##### Dodawanie kolumn/wierszy

Najprostszym sposobem na dodanie kolumny/wiersza do struktury `DataFrame` jest przypisanie wartości do nieistniejącej kolumny/wiersza, przykładowo:

```python
trig["New column"] = -1
```

```python
trig.loc[1337, :] = -1
```

##### Zmiana indeksu

Możliwa jest zmiana wartości indeksu wierszy `DataFrame` poprzez użycie metody `set_index`. Przykładowo, jeśli chcemy wykorzystać wartości znajdujące się w kolumnie *sinus* jako indeks:

```python
trig.set_index(trig["sinus"], inplace=True)
```

Zwróć uwagę na dodatkowy parametr `inplace` - wiele metod `DataFrame` domyślnie nie modyfikuje obiektu, na którym je wywołujemy, tylko zwraca nowy obiekt, co oznacza, że musielibyśmy zapisać wynik z powrotem do zmiennej:

```python
trig = trig.set_index(trig["sinus"])
```

Dodanie parametru `inplace=True` powoduje, że operacja jest wykonywana "w miejscu". Przy korzystaniu z nowych metod modyfikujących `DataFrame` sprawdź w dokumentacji, jakie jest ich zachowanie. 

##### Zmiana nazw kolumn

Zmiana nazw kolumn możliwa jest w wygodny sposób metodą `rename` na podstawie słownika ze zbiorem wpisów `"stara_nazwa": "nowa_nazwa"` przekazanego do parametru `columns`.

```python
rename_dict = {"sinus": "sin", "cosinus": "cos"}

trig.rename(columns=rename_dict, inplace=True)
```

Analogicznie jak przy `set_index` metoda możliwa jest zmiana "w miejscu" lub zwrócenie nowego `DataFrame`.

##### Sortowanie

Sortowanie tabeli sprowadza się zazwyczaj do uruchomienia jednej metody, w której podajemy etykietę (lub listę etykiet), po których będą sortowane dane i opcjonalne dodatkowe parametry.

```python
trig.sort_values("cos", axis=0, inplace=True, ascending=False)  # sortowanie wzdłuż osi 0 (po wierszach), w miejscu, malejąco
```

### Odczyt i zapis do plików

Pandas obsługuje odczyt i zapis danych z wielu różnych formatów.

Jeśli chcemy przenosić dane pommiędzy różnymi programami lub publikować warto wykorzystać format `CSV`, ze względu na prostotę i przenośność.

Eksport do pliku CSV możliwy jest metodą `to_csv(filename)` na obiekcie `DataFrame`:

```python
trig.to_csv("trig.csv")
```

Wczytanie istniejącego pliku odbywa się funkcją `pd.read_csv(filename)`. Jeśli chcemy, aby kolumna w pliku została potraktowana jako indeks, musimy przekazać jej położenie do opcjonalnego argumentu `index_col`:

```python
trig_from_csv = pd.DataFrame(pd.read_csv("trig.csv", index_col=0))  # read_csv() może zwracać nie tylko DataFrame przekazanie do konstruktora usprawni podpowiadanie składni w IDE
```

Jeśli planujemy zachować np. wstępnie przetworzone dane do dalszej analizy lub wykorzystania w innym programie obsługującym ten format, warto wykorzystać format `HDF5` dedykowany do danych tabelarycznych. Pozwala on przechowywać bardziej zaawansowane typy danych, jest także szybszy w parsowaniu i pozwala na opcjonalną kompresję:

```python
trig.to_hdf("trig.hdf5", "data", format="fixed", mode="w", complevel=5)  # zapis

trig_from_hdf = pd.DataFrame(pd.read_hdf("trig.hdf5"))
```

---

## 🔥 Zadanie końcowe 🔥

1. Wczytaj dostarczony plik [population_by_country_2019_2020.csv](_resources/lab_01/population_by_country_2019_2020.csv) do `DataFrame`. (źródło: https://www.kaggle.com/tanuprabhu/population-by-country-2020).

2. Zbadaj zawartość tabeli wyświetlając ją w GUI oraz wyświetlając podsumowanie w konsoli Pythona.

3. Policz bezwzględną i względną zmianę populacji w 2020 w stosunku do roku 2019 i umieść w nowych kolumnach, odpowiednio `Net population change` i `Population change [%]`.

4. Posortuj dane pod kątem względnej zmiany populacji.

5. Wygeneruj wykres typu "bar" 10 krajów, które miały największy procentowy przyrost populacji. Zawrzyj na nim populacje z 2019 i 2020. Do wyboru kolumn użyj filtra z wyrażeniem regularnym.

6. Dodaj kolejną kolumnę `Density (2020)` i wpisz w niej słowo "Low".

7. Policz gęstość zaludnienia i w krajach, gdzie przekracza 500 osób na km<sup>2</sup> wpisz w kolumnie `Density` słowo "High".

8. Wybierz co drugi kraj i zapisz do nowego pliku **population_output.csv**.

---

---
Autorzy: *Jakub Tomczyński*
