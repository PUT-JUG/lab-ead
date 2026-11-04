"""Projekt 1 (Lab 05) - imiona w USA i w Polsce.

Szablon rozwiązania. Zachowaj nazwy i sygnatury funkcji oznaczonych jako
WYMAGANE - są one sprawdzane automatycznie. Możesz (i powinieneś) dopisywać
własne funkcje pomocnicze, w tym funkcje rysujące wykresy.

Zasady:
- funkcje WYMAGANE nie mogą modyfikować przekazanych ramek danych,
- funkcje WYMAGANE nie mogą niczego wyświetlać ani rysować - tylko liczą,
- cały kod wykonujący obliczenia dla zadań uruchamia się z funkcji main(),
- dozwolone biblioteki: biblioteka standardowa, numpy, pandas, matplotlib,
  seaborn, duckdb.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# --- wklej tu wynik polecenia: python parametry.py <nr_indeksu> ---
STUDENT_ID = "000000"
PARAMS = {
    "top_n": 1000,
    "top_k_male": 15,
    "annot_year": 2025,
    "coverage_q": 0.5,
    "length_sex": "F",
    "length_years": [1900, 1960, 2025],
    "min_decade_births": 1000,
    "pl_top_n": 200,
}
# -------------------------------------------------------------------

DATA_DIR = Path("./data")
PL_DB = DATA_DIR / "names_pl_2000-25.sqlite"
OUT_DIR = Path("./wyniki")


# =========================================================================
# Funkcje WYMAGANE (sprawdzane automatycznie)
# =========================================================================

def load_usa(data_dir) -> pd.DataFrame:
    """Pkt 1. Wczytuje wszystkie pliki yobRRRR.txt z katalogu data_dir.

    Zwraca ramkę z kolumnami: name (str), sex ('F'/'M'), year (int),
    decade (int, np. 1987 -> 1980), count (int).
    Wiersze posortowane: year rosnąco, sex rosnąco (F przed M), count malejąco.
    Indeks: 0, 1, 2, ... (RangeIndex). Inne pliki w katalogu są ignorowane.
    """
    raise NotImplementedError


def name_stats(df: pd.DataFrame) -> dict:
    """Pkt 2. Zwraca słownik z kluczami:

    - "unique_total": liczba unikalnych imion (imię nadawane obu płciom liczone raz),
    - "unique_F", "unique_M": liczba unikalnych imion danej płci,
    - "one_year_F", "one_year_M": liczba imion danej płci, które wystąpiły
      (dla tej płci) tylko w jednym roku,
    - "new_per_decade": słownik {dekada: liczba imion, które po raz pierwszy
      pojawiły się w zbiorze w tej dekadzie (bez rozróżnienia płci)},
      tylko dekady z wartością > 0, klucze typu int.
    Wszystkie wartości typu int.
    """
    raise NotImplementedError


def add_frequency_rank(df: pd.DataFrame) -> pd.DataFrame:
    """Pkt 3. Zwraca kopię df z dodanymi kolumnami:

    - frequency: count / suma count dla danego (year, sex),
    - rank: pozycja w rankingu danego (year, sex), 1 = największe count;
      równe count -> ta sama, najniższa pozycja (1, 2, 2, 4, ...); typ int.
    Musi działać dla ramki zawierającej tylko kolumny name, sex, year, count.
    """
    raise NotImplementedError


def unique_per_year(df: pd.DataFrame) -> pd.DataFrame:
    """Pkt 4. Liczba unikalnych imion w każdym roku.

    Zwraca ramkę: indeks year (int, rosnąco), kolumny "F" i "M" (int).
    """
    raise NotImplementedError


def peak_ranking(df: pd.DataFrame, n: int) -> dict:
    """Pkt 5. Ranking top-n imion wg szczytowej popularności.

    df zawiera kolumnę frequency (wynik add_frequency_rank).
    Zwraca słownik {"F": ramka, "M": ramka}; każda ramka ma indeks name
    i kolumny peak (maksymalna frequency) oraz peak_year (int, rok szczytu;
    przy remisie najwcześniejszy). Posortowane malejąco wg peak (przy remisie
    alfabetycznie wg name), co najwyżej n wierszy.
    """
    raise NotImplementedError


def coverage(df: pd.DataFrame, q: float) -> pd.DataFrame:
    """Pkt 7. Miara różnorodności.

    Dla każdego (year, sex): najmniejsza liczba k najczęściej nadawanych imion,
    dla której suma ich count >= q * (suma count w danym year i sex).
    Zwraca ramkę: indeks year (int, rosnąco), kolumny "F" i "M" (int).
    """
    raise NotImplementedError


def mean_name_length(df: pd.DataFrame) -> pd.DataFrame:
    """Pkt 8. Średnia długość imienia (liczba znaków) ważona count.

    Zwraca ramkę: indeks year (int, rosnąco), kolumny "F" i "M" (float).
    """
    raise NotImplementedError


def length_distribution(df: pd.DataFrame, sex: str, years: list) -> pd.DataFrame:
    """Pkt 8. Rozkład długości imion dla płci sex w latach years.

    Zwraca ramkę: indeks - długość imienia (int, rosnąco), kolumny - lata
    (int, w kolejności z years); wartość = udział urodzeń z imionami danej
    długości wśród urodzeń płci sex w danym roku (każda kolumna sumuje się
    do 1, brak imion danej długości -> 0).
    """
    raise NotImplementedError


def decade_connotation(df: pd.DataFrame, ranking: dict, min_births: int) -> pd.DataFrame:
    """Pkt 9. Zmiana konotacji imion w dekadach.

    Uwzględnia imiona obecne jednocześnie w ranking["F"] i ranking["M"]
    (wynik peak_ranking). df zawiera kolumnę decade.
    Zwraca ramkę z indeksem (name, decade), posortowaną wg name i decade,
    z kolumnami:
    - F, M: łączna liczba nadań imienia danej płci w dekadzie (int),
    - w_m: M / (F + M),
    - dw: w_m minus w_m z poprzedniego wiersza tego samego imienia
      (NaN dla pierwszej dekady imienia).
    Wiersze z F + M < min_births są usuwane PRZED wyznaczeniem dw.
    """
    raise NotImplementedError


def load_pl(db_path) -> pd.DataFrame:
    """Pkt 10. Wczytuje dane polskie JEDNYM zapytaniem SQL.

    Zwraca ramkę z kolumnami: name, sex ('F'/'M'), year, count, frequency,
    gdzie frequency jest wyznaczona w zapytaniu SQL (count / suma count
    dla danego year i sex). Sortowanie jak w load_usa.
    """
    raise NotImplementedError


# =========================================================================
# Funkcje pomocnicze, wykresy itd. - według własnego uznania
# =========================================================================

def save_results(results: dict, out_dir: Path) -> None:
    """Zapisuje słownik wyników do out_dir/results.json (konwertuje typy numpy)."""
    def convert(o):
        if hasattr(o, "item"):
            return o.item()
        raise TypeError(f"Nieobsługiwany typ: {type(o)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=convert)


# =========================================================================
# main
# =========================================================================

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = {"student_id": STUDENT_ID, "params": PARAMS}

    # Wymagana struktura results (wartości uzupełnij wynikami obliczeń).
    # Przy remisach wybieraj pierwszą wartość (najwcześniejszy rok itd.).
    results["p2"] = None  # wynik name_stats(...)
    results["p4"] = {"min_year": None, "min_ratio": None,
                     "max_year": None, "max_ratio": None}
    results["p5"] = {"F": [], "M": []}  # po 5 słowników {"name", "peak", "peak_year"}
    results["p6"] = {"female_name": None, "male_name": None, "male_peak_year": None,
                     "female_count_annot": None, "male_count_annot": None}
    results["p7"] = {"max_diff_year": None, "max_diff": None}  # max |F - M|
    results["p8"] = {"max_increase_length": None, "max_decrease_length": None}
    results["p9"] = {"max_decrease": {"name": None, "decade": None, "dw": None},
                     "max_increase": {"name": None, "decade": None, "dw": None}}
    results["p10"] = {"top_F": [], "top_M": [],  # po 5 pierwszych imion z rankingu PL
                      "last_F": None, "last_M": None,  # ostatnie (pl_top_n-te) imię rankingu PL
                      "frequency_max_abs_diff": None}  # max |frequency SQL - pkt 3|
    results["answers"] = {"p7": "", "p10_diversity": "", "p10_length": ""}

    # Wykresy zapisz do OUT_DIR pod nazwami:
    # fig_04.png, fig_06.png, fig_07.png, fig_08a.png, fig_08b.png,
    # fig_09.png, fig_10a.png, fig_10b.png

    save_results(results, OUT_DIR)
    plt.show()


if __name__ == "__main__":
    main()
