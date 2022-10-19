# Lab 02 - modyfikacja i augmentacja, bazy danych, REST API

## Bazy danych SQL

Wiele systemów informatycznych przechowuje informacje w formie *baz danych* - m.in. portale internetowe, systemy magazynowe, systemy logowania danych (np. automatyki budynkowej) itp.

Najpopularniejszą dziś grupę stanowią bazy danych wykorzystujące język zapytań *SQL* (ang. *Structured Query Language*) - dostępne są różne implementacje takie jak *MySQL*, *Oracle*, *PostgreSQL*. Każda z nich stanowi oddzielną, niezależną implementację i ma własny format zapisu oraz specyficzne rozwiązania, ale łączy je wspomniany wcześniej, w dużej mierze kompatybilny język zapytań.

We wspomnianych wcześniej rozwiązaniach, gdzie do bazy musi mieć dostęp wielu klientów jednocześnie, w dostępie pośredniczy zazwyczaj serwer, z którym klienty komunikują się poprzez protokoły sieciowe. W ramach zajęć dla uproszczenia wykorzystamy lekką implementację *SQLite* i będziemy operować bezpośrednio na pliku zawierającym całą bazę, jednak te same polecenia łatwo *przeportować* na pełnoprawny system z dostępem równoległym.

W poniższych przykładach zostaną zaprezentowane podstawowe, najczęściej wykorzystywane zapytania SQL. Po bardziej rozbudowane przykłady i opisy komend warto sięgnąć do tutoriala o SQL, np. https://www.sqlitetutorial.net

### Przeglądarki SQLite

Często aby poznać strukturę czy zweryfikować zawartość bazy warto użyć przeglądarki wyposażonej w GUI. Dostępne są różne programy, m.in. darmowe:

* DB Browser for SQLite (Windows/macOS/Linux): https://sqlitebrowser.org/dl/
* Datum - Lite (Windows/macOS)

### SQLite w Python - `sqlite3`

Do komunikacji z bazą danych wykorzystamy pakiet `sqlite3`. Pełną dokumentację wraz z przykładami można znaleźć pod poniższym linkiem: https://docs.python.org/3/library/sqlite3.html

Podczas kursu skupimy się na odczycie danych z bazy, ale biblioteka pozwala też oczywiście na zapis.

Pobierz przykładową bazę danych ze sklepu sprzedającego albumy muzyczne: https://github.com/lerocha/chinook-database#how-do-i-download-and-create-the-chinook-database

Pobierz z sekcji *Downloads* plik `Chinook_Sqlite.sqlite`. Otwórz pobrany plik w wybranej przeglądarce SQLite i pobieżnie przejrzyj strukturę bazy danych, zawarte w niej tabele i informacje.

Stwórz skrypt Pythona i zaimportuj bibliotekę `sqlite3`. Następnie wykonaj poniższy kod - przykładową operację odczytu wszystkich danych z tabeli `Album`

```python
conn = sqlite3.connect("Chinook_Sqlite.sqlite")  # połączenie do bazy danych - pliku
c = conn.cursor()

for row in c.execute('SELECT * FROM Album'):
    print(row)

conn.close()
```

#### `SELECT`, `WHERE`, `ORDER BY`

Połączenie do bazy - pliku oraz pobranie *kursora* do połączenia wykonujemy raz przed operacjami na bazie danych. Właściwe operacje przekazywane są jako tekst do metody `execute` kursora, mamy w związku z tym do czynienia z "zagnieżdżeniem" języków programowania. Powyższy przykład uruchamia najczęściej wykorzystywaną w SQL komendę `SELECT`, służącą do pobierania danych i odczytuje wszystkie kolumny (`*`) z tabeli `Album`. W tym przypadku `execute` zwraca iterowalny obiekt, w którym każdy z elementów jest krotką - wierszem z tabeli.

Ponieważ zmiana układu tabeli w bazie danych spowodowałaby, że dane zostaną zwrócone w innym układzie. W związku z tym w kodzie innym niż testowy nigdy nie powinno pojawić się tego typu zapytanie. Zamiast tego możemy podać jawnie nazwy kolumn:

```sql
SELECT AlbumID, ArtistID, Title FROM Album
```

Komendę `SELECT` można rozbudować o klauzulę `WHERE`, która pozwala odfiltrować dane po wybranym kryterium, zgodnie z wzorcem `SELECT column_list FROM table WHERE search_condition;`, np:

```sql
WHERE column = 100;
WHERE column IN (1,2,3) AND other_column = 50;
WHERE column LIKE 'An%';
WHERE column BETWEEN 10 AND 20;
```

Inną klauzulą, jaką można dodać do komendy `SELECT` jest `ORDER BY` powodujące sortowanie po określonej kolumnie/kolumnach.

```sql
ORDER BY column;
```

Opcjonalnie można podać kierunek sortowania (domyślnie rosnąco - `ASC`):

```sql
ORDER BY column ASC;
ORDER BY column DESC;
```

Klauzule można łączyć w złożone zapytania, np:

```sql
SELECT ArtistId, Name FROM Artist WHERE ArtistID BETWEEN 20 and 40 ORDER BY Name;
```

---

#### 🔥 Zadanie 1 🔥

Pobierz z tabeli **Invoice** listę transakcji (zawierającą **InvoiceId**, **CustomerId**, **BillingCity** oraz **Total** z kraju **USA**, sortując wpisy po nazwie miasta, w kolejności odwrotnej do alfabetycznej.

Wyświetl wpisy w konsoli w postaci:

```
invoice: 14, customer: 17, city: Redmond, total: 1.98
invoice: 13, customer: 16, city: Mountain View, total: 0.99
invoice: 5, customer: 23, city: Boston, total: 13.86
```

---

#### `JOIN`

Ponieważ dane w bazach SQL przechowywane są w tylko formacie dwuwymiarowych tabel, konieczna jest możliwość tworzenia relacji pomiędzy poszczególnymi tabelami oraz ekstrakcji danych zawartych w kilku tabelach. Przykładowo, w omawianej bazie danych tabela `Invoice` nie zawiera informacji o pozycjach na paragonie, ale możemy je odnaleźć w tabeli `InvoiceLine`, wiążąc pozycje z obu tabeli za pomocą `InvoiceId`, które jest unikalne dla każdego paragonu. Analogicznie, w tabeli z albumami nie ma zawartej nazwy wykonawcy (która nie musi być unikalna), znajdują się tam jedynie indeksy `ArtistId` korespondujące z wierszami w tabeli `Artist`.

Do połączenia informacji z różnych tabel wykorzystamy komendę `JOIN`. Komenda może pracować w różnych trybach, dwa które będziemy wykorzystywać to `INNER JOIN` oraz `LEFT JOIN`.

`INNER JOIN` pobiera część wspólną tabel, łącząc wpisy po wybranym kryterium:

---

**Table_A**:

| foos | id |
|------|----|
| f1   | 1  |
| f2   | 2  |
| f3   | 3  |

**Table_B**:

| bars | id |
|------|----|
| b1   | 1  |
| b2   | 2  |
| b3   | 5  |

```sql
SELECT foos, bars FROM Table_A INNER JOIN Table_B ON Table_A.id = Table_B.id
```

Wynik:

| bars | foos |
|------|----|
| b1   | f1  |
| b2   | f2  |

---

Przykładowo, aby uzyskać nazwy wykonawców przyporządkowane do tytułów albumów:

```sql
SELECT Track.Name, Album.Title FROM Track INNER JOIN Album ON Track.AlbumId = Album.AlbumId
```

Zwrócona tabela będzie zawierała tytuły piosenek pobrane z tabeli **Track**, tytuły albumów z tabeli **Album**, a wpisy zostaną dopasowane na podstawie kolumny **AlbumId** - kryterium `Track.AlbumId = Album.AlbumId`. Zwrócone zostaną tylko te wpisy, które istnieją w obu tabelach.

Po bardziej rozbudowane przykłady zajrzyj do https://www.sqlitetutorial.net/sqlite-inner-join/

`LEFT JOIN` zwróci wszystkie wpisy znajdujące się w pierwszym argumencie. Brakujące wartości zostaną wypełnione wartościami `NULL`:

---

**Table_A**:

| foos | id |
|------|----|
| f1   | 1  |
| f2   | 2  |
| f3   | 3  |

**Table_B**:

| bars | id |
|------|----|
| b1   | 1  |
| b2   | 2  |
| b3   | 5  |

```sql
SELECT foos, bars FROM Table_A LEFT JOIN Table_B ON Table_A.id = Table_B.id
```

Wynik:

| bars | foos |
|------|----|
| b1   | f1  |
| b2   | f2  |
| b3   | NULL  |

---

#### 🔥 Zadanie 2 🔥 

Stwórz zapytanie SQL do bazy, dzięki któremu uzyskasz listę albumów wraz z ich wykonawcą.

Przetestuj różne formy `JOIN` (`INNER` oraz `LEFT`), dla wariantu `LEFT` sprawdź wynik w sytuacjach kiedy pierwszym argumentem jest tablica z albumami oraz tablica z wykonawcami. Zatanów się z czego wynikają różnice.

---

## REST API, usługi RESTful

*REST* to koncepcja architektury oprogramowania usług internetowych. Głównym założeniem jest to, że usługi takie są bezstanowe, tzn. każdy pakiet transmisji stanowi samodzielną całość, która może być zrozumiana bez informacji z poprzednich pakietów - pakiety nie układają się w "rozmowę".

Koncepcja nie definiuje standardu protokołu, ale najczęściej wykorzystywany protokół do komunikacji to HTTP (z metodami GET, POST, PUT itd.), a sama zawartość wiadomości sformatowana jest jako najczęściej jako JSON, XML lub HTML.

Do obsługi zapytań HTTP w Python wykorzystamy bibliotekę `requests`.

W ramach pierwszego przykładu sprawdźmy aktualne kursy Bitcoin korzystając z API opisanego na stronie https://www.blockchain.com/api/exchange_rates_api

```python
req = requests.get("https://blockchain.info/ticker")  # wysłanie zapytania GET pod odpowiedni adres, zapisanie odpowiedzi
print(req.text)  # zawartość odpowiedzi znajduje się w polu text
```

Odpowiedź zwracana jest w formacie JSON (JavaScript Object Notation). Format wywodzi się z JavaScript i bardzo często wykorzystywany w zastosowaniach webowych czy IoT, niekoniecznie w powiązaniu z JS. JSON pozwala na przesłanie danych w formie par klucz-wartość jako ciągłego tekstu, która jednocześnie jest czytelna dla człowieka i może być sparsowana przez program. W Python format ten bardzo dobrze tłumaczy się z/na natywne słowniki przez moduł `json`:

```python
bitcoin_dict = json.loads(req.text)
```

Z tak skonwertowanego słownika możemy już korzystać w standardowy sposób:

```python
print(bitcoin_dict['USD']['last'])
```

Wykorzystanie modułu `json` sprowadza się do znajomości czterech metod:

* `load`: plik JSON → słownik Python
* `loads`: string JSON → słownik Python
* `dump`: słownik Python → plik JSON
* `dumps`: słownik Python → string JSON

---

#### 🔥 Zadanie 3 🔥 

Stwórz na podstawie powyższego zapytania DataFrame, w którym umieścisz wszystkie odebrane dane. Indeksem powinny być trzyznakowe symbole waluty, a kolumnami wartości kursów oraz symbol waluty (`15m`, `last`, `buy`, `sell`, `symbol`).

---

### OpenWeather API

Świadczenie usług webowych wymaga oczywiście utrzymania infrastruktury serwerowej, w związku z czym wiele serwisów prowadzonych jest jako działalność komercyjna, gdzie część lub całość dostępu wymaga wykupienia dostępu lub przynajmniej utworzenia konta. Autoryzacja odbywa się często z wykorzystaniem *tokenu*, indywidualnego dla użytkownika.

Jako przykładowe API wymagające autoryzacji wykorzystamy serwis z pogodą https://openweathermap.org/api

1. Stwórz darmowe konto w serwisie (*Sign In* → *Create an Account*)

2. Przejdź do sekcji *API Keys* w koncie użytkownika. Stwórz nowy klucz o wybranej nazwie do wykorzystania podczas zajęć. Tworzenie odrębnych kluczy dla różnych aplikacji daje elastyczną kontrolę nad nimi (można usunąć dostęp dla jednej aplikacji przez wycofanie konkretnego klucza). Skopiuj klucz w bezpieczne miejsce.

Przetestuj działanie swojego klucza wykonując zapytanie do Open Weather One Call API (dokumentacja: https://openweathermap.org/api/one-call-api). Zapytanie konstruowane jest w formie Query string, z argumentami przekazywanymi w formie `arg1=wartosc1&arg2=wartosc2` itd:

```python
url = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "TWOJ_API_KEY"
latitude = 37.2431
longitude = -115.7930
req = requests.get(f"{url}?lat={latitude}&lon={longitude}&exclude=minutely&appid={api_key}")
print(req.text)
```

**Uwaga!** w darmowej wersji konta liczba zapytań do One Call API jest ograniczona do 1000 dziennie i 60 na minutę. O ile program ogranicza się do pojedynczego zapytania, nie powinno stanowić to problemu, jednak kiedy odpytujemy np. wiele lokalizacji w pętli lub prowadzimy testy programu możemy szybko osiągnąć ten limit.
W czasie oczekiwania na generację klucza, można skorzystać z [dumpu wyniku](_resources/lab_02/ow.dump.json) wygenerowanego przez zapytanie.

Zapisz uzyskaną odpowiedź do pliku tekstowego `weather_forecast.json`.

💡**Podpowiedź**💡

Bardzo wygodną przeglądarką plików JSON jest Firefox - spróbuj otworzyć w nim zapisany plik i przeanalizuj strukturę odpowiedzi.

---

#### 🔥 Zadanie 4 🔥 

1. Sprawdź lokalizację (długość i szerokość geograficzną) swojego ulubionego miasta i odpytaj API o prognozę pogody dla niego.

2. Zwróć uwagę na odczytane temperatury. Sprawdź w dokumentacji jak przełączyć jednostki na metryczne i popraw zapytanie.

3. Przepisz informacje z prognozy godzinnej (pole `hourly`) odczytanego JSON-a do DataFrame. Umieść w DataFrame kolumny takie jak `temp`, `feels_like`, `humidity`, `wind_speed`. Zwróć uwagę na pola `dt` w uzyskanej odpowiedzi - są to znaczniki czasu w formacie UNIX (sekundy liczone od 00:00:00 UTC on 1 January 1970). Skonwertuj znaczniki na format `Datetime` pandasa, wykorzystując funkcję `pd.to_datetime`: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html

4. Wykreśl prognozę pogody na wykresie liniowym korzystając z metody `pd.DataFrame.plot`

---


# 🔥 Zadanie końcowe - Pokédex 🔥

Budujesz urządzenie, które będzie zawierało informacje o znalezionych przez Ciebie Pokemonach. Informacje o spotkanych stworzeniach zapisujesz w DataFrame wraz z datą i miejscem pierwszego spotkania.

Dotychczasowe dane zapisane są w pliku [pokedex_history.hdf5](_resources/lab_02/pokedex_history.hdf5)

Udało Ci się znaleźć dwa źródła danych, którymi możesz uzupełnić posiadane informacje:

- Usługę PokéAPI, które możesz odpytywać o umiejętności i podstawowe statystyki: https://pokeapi.co
- bazę danych [pokemon_against.sqlite](_resources/lab_02/pokemon_against.sqlite) zawierającą informacje o skuteczności w walce z Pokemonami innych typów

Dla wszystkich spotkanych Pokemonów
1. Pobierz z PokéAPI informację o statystykach dla danego Pokemona: **hp**, **attack**, **defense**, **special-attack**, **special-defense**, **speed** i umieść w DataFrame. Odczytaj też informacje o typach danego Pokemona i umieść je w kolumnach **type_1** i **type_2**. Jeśli dany Pokemon ma tylko jeden typ, wpisz wartość `None`.

2. Z bazy danych odczytaj informację z kolumn **against_\*** mówiącą o skuteczności ataku

3. Napisz funkcję `attack_against(attacker: str, attacked: str, database: pd.DataFrame)` zwracającą skuteczność ataku Pokemona o nazwie `attacker` na Pokemona o nazwie `attacked`. Jeśli w bazie nie będzie wystarczających informacji zwracaj wartość `None`.

---
Autorzy: *Jakub Tomczyński*
