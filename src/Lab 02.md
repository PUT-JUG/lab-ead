# Lab 02 - modyfikacja i augmentacja, bazy danych, REST API

## Bazy danych SQL

Wiele systemów informatycznych przechowuje informacje w formie *baz danych* - m.in. portale internetowe, systemy magazynowe, systemy logowania danych (np. automatyki budynkowej) itp.

Najpopularniejszą dziś grupę stanowią bazy danych wykorzystujące język zapytań *SQL* (ang. *Structured Query Language*) - dostępne są różne implementacje takie jak *MySQL*, *Oracle*, *PostgreSQL*. Każda z nich stanowi oddzielną, niezależną implementację i ma własny format zapisu oraz specyficzne rozwiązania, ale łączy je wspomniany wcześniej, w dużej mierze kompatybilny język zapytań.

We wspomnianych wcześniej rozwiązaniach, gdzie do bazy musi mieć dostęp wielu klientów jednocześnie, w dostępie pośredniczy zazwyczaj serwer, z którym klienty komunikują się poprzez protokoły sieciowe. W ramach zajęć dla uproszczenia wykorzystamy lekką implementację *SQLite* i będziemy operować bezpośrednio na pliku zawierającym całą bazę, jednak te same polecenia łatwo *przeportować* na pełnoprawny system z dostępem równoległym.

### Przeglądarki SQLite

Często aby poznać strukturę czy zweryfikować zawartość bazy warto użyć przeglądarki wyposażonej w GUI. Dostępne są różne programy, m.in. darmowe:

* DB Browser for SQLite (Windows/macOS/Linux): https://sqlitebrowser.org/dl/
* Datum - Lite (Windows/macOS)


### SQLite w Python - `sqlite3`

Do komunikacji z bazą danych wykorzystamy pakiet `sqlite3`. Pełną dokumentację wraz z przykładami można znaleźć pod poniższym linkiem: https://docs.python.org/3/library/sqlite3.html

Podczas kursu skupimy się na odczycie danych z bazy, ale biblioteka pozwala też oczywiście na zapis.

Pobierz przykładową bazę danych zawierającą log czujników temperatury i wilgotności w pomieszczeniu: TODO LINK



## REST API




---
Autorzy: *Jakub Tomczyński*
