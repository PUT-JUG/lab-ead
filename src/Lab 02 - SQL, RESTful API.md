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

Połączenie do bazy - pliku oraz pobranie *kursora* do połączenia wykonujemy raz przed operacjami na bazie danych. Właściwe operacje przekazywane są jako tekst do metody `execute` kursora. Powyższy przykład uruchamia najczęściej wykorzystywaną w SQL komendę `SELECT`, służącą do pobierania danych i odczytuje wszystkie kolumny (`*`) z tabeli `Album`. W tym przypadku `execute` zwraca iterowalny obiekt, w którym każdy z elementów jest krotką - wierszem z tabeli.

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

#### 🔥 Zadanie 🔥

Pobierz z tabeli `Invoice` listę transakcji (zawierającą **InvoiceId**, **CustomerId**, **BillingCity** oraz **Total** z kraju `USA`, sortując wpisy po nazwie miasta, w kolejności odwrotnej do alfabetycznej.

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
SELECT Album.Title, Artist.Name FROM Album INNER JOIN Artist ON Artist.ArtistId = Album.ArtistId;
```

Zwrócona tabela będzie zawierała tytuł albumu pobrany z tabeli `Album`, nazwę artysty z tabeli `Artist`, a wpisy zostaną dopasowane na podstawie kolumny `ArtistId` - kryterium `Artist.ArtistId = Album.ArtistId`. Zwrócone zostaną tylko te wpisy, które istnieją w obu tabelach. 

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

#### 🔥 Zadanie 🔥 TODO

Pobierz z tabeli `Invoice` listę transakcji (zawierającą **InvoiceId**, **CustomerId**, **BillingCity** oraz **Total** z kraju `USA`, sortując wpisy po nazwie miasta, w kolejności odwrotnej do alfabetycznej.

Wyświetl wpisy w konsoli w postaci:

```
invoice: 14, customer: 17, city: Redmond, total: 1.98
invoice: 13, customer: 16, city: Mountain View, total: 0.99
invoice: 5, customer: 23, city: Boston, total: 13.86
```

---

## REST API




---
Autorzy: *Jakub Tomczyński*
