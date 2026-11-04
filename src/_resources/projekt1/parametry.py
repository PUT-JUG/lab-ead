"""Generator indywidualnych parametrów do projektu 1 (Lab 05).

Użycie:
    python parametry.py 123456

Skrypt wypisuje blok STUDENT_ID / PARAMS, który należy wkleić na początek
własnego rozwiązania (w miejsce bloku z szablonu). Parametry zależą tylko
od numeru indeksu - każde uruchomienie daje ten sam wynik.
"""

import hashlib
import json
import sys

SALT = "EDA-projekt1-2026"


def get_params(student_id: str) -> dict:
    """Zwraca słownik parametrów wyznaczony deterministycznie z numeru indeksu."""
    student_id = str(student_id).strip()
    if not student_id.isdigit():
        raise ValueError(f"Numer indeksu powinien składać się z cyfr: {student_id!r}")
    h = int(hashlib.sha256(f"{SALT}:{student_id}".encode()).hexdigest(), 16)

    def pick(options):
        nonlocal h
        h, r = divmod(h, len(options))
        return options[r]

    return {
        "top_n": pick([500, 750, 1000]),            # pkt 5, 9 - wielkość rankingu USA
        "top_k_male": pick([8, 10, 15, 22, 30]),    # pkt 6 - ile pierwszych imion męskich rozważyć
        "annot_year": pick([2015, 2020, 2025]),     # pkt 6 - rok opisu liczby nadań
        "coverage_q": pick([0.4, 0.45, 0.5, 0.55, 0.65, 0.7]),  # pkt 7, 10 - udział urodzeń
        "length_sex": pick(["F", "M"]),             # pkt 8 - płeć dla rozkładu długości
        "length_years": [pick([1890, 1900, 1910, 1920]),
                         pick([1950, 1960, 1970]),
                         2025],                     # pkt 8 - lata rozkładu długości
        "min_decade_births": pick([500, 1000, 2000]),  # pkt 9 - próg nadań w dekadzie
        "pl_top_n": pick([100, 150, 200]),          # pkt 10 - wielkość rankingu PL
    }


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    student_id = sys.argv[1].strip()
    params = get_params(student_id)
    print("# --- wklej do swojego skryptu ---")
    print(f'STUDENT_ID = "{student_id}"')
    print("PARAMS = " + json.dumps(params, indent=4))


if __name__ == "__main__":
    main()
