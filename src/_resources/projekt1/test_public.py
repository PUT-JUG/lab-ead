"""Publiczne testy do projektu 1 (Lab 05).

Użycie (z katalogu, w którym jest Twój skrypt i podkatalog ./data):
    python test_public.py moj_projekt.py          # testy funkcji na małych danych
    python test_public.py moj_projekt.py --full   # + uruchomienie całego skryptu

Testy sprawdzają zgodność z interfejsem z szablonu na małym, ręcznie
policzonym przykładzie. Zaliczenie testów publicznych NIE oznacza
poprawności całego rozwiązania - przy ocenie używane są dodatkowe testy.
"""

import importlib.util
import json
import math
import os
import sqlite3
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

REQUIRED_FUNCS = ["load_usa", "name_stats", "add_frequency_rank", "unique_per_year",
                  "peak_ranking", "coverage", "mean_name_length", "length_distribution",
                  "decade_connotation", "load_pl", "main"]
FIGURES = ["fig_04.png", "fig_06.png", "fig_07.png", "fig_08a.png", "fig_08b.png",
           "fig_09.png", "fig_10a.png", "fig_10b.png"]
RESULT_KEYS = {
    "p2": ["unique_total", "unique_F", "unique_M", "one_year_F", "one_year_M", "new_per_decade"],
    "p4": ["min_year", "min_ratio", "max_year", "max_ratio"],
    "p5": ["F", "M"],
    "p6": ["female_name", "male_name", "male_peak_year", "female_count_annot", "male_count_annot"],
    "p7": ["max_diff_year", "max_diff"],
    "p8": ["max_increase_length", "max_decrease_length"],
    "p9": ["max_decrease", "max_increase"],
    "p10": ["top_F", "top_M", "last_F", "last_M", "frequency_max_abs_diff"],
    "answers": ["p7", "p10_diversity", "p10_length"],
}

# ---------------------------------------------------------------- dane testowe
YOB = {
    1880: "Anna,F,10\nMary,F,6\nJohn,M,8\nAnna,M,2\n",
    1881: "Mary,F,9\nAnna,F,3\nLu,F,3\nJohn,M,5\n",
    1890: "Mary,F,4\nKim,F,4\nKim,M,6\nJohn,M,4\nAnna,M,3\n",
}


def make_usa_dir(tmp: Path) -> Path:
    d = tmp / "usa"
    d.mkdir()
    for year in sorted(YOB, reverse=True):
        (d / f"yob{year}.txt").write_text(YOB[year])
    (d / "NationalReadMe.pdf").write_text("to nie są dane")
    return d


def make_pl_db(tmp: Path) -> Path:
    path = tmp / "pl.sqlite"
    with sqlite3.connect(path) as c:
        for table, sex, rows in [
            ("females", "K", [(2001, "ANNA", 5), (2000, "EWA", 10), (2000, "ANNA", 30)]),
            ("males", "M", [(2001, "JAN", 15), (2000, "JAN", 20), (2001, "ANNA", 5)]),
        ]:
            c.execute(f'CREATE TABLE {table} ("Rok" INTEGER, "Imię" TEXT, "Liczba" INTEGER, "Płeć" TEXT)')
            c.executemany(f"INSERT INTO {table} VALUES (?, ?, ?, ?)",
                          [(r, n, k, sex) for r, n, k in rows])
    return path


# ---------------------------------------------------------------- pomocnicze
def close(a, b, tol=1e-9):
    return math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)


def as_rows(df, cols):
    return [tuple(r) for r in df[cols].itertuples(index=False)]


def check_table(res, index, columns, values, what):
    assert list(map(int, res.index)) == index, f"{what}: indeks {list(res.index)} != {index}"
    assert [str(c) for c in res.columns] == [str(c) for c in columns], \
        f"{what}: kolumny {list(res.columns)} != {columns}"
    for i, row in zip(index, values):
        for c, v in zip(columns, row):
            got = res.loc[i, c]
            assert close(got, v, 1e-6), f"{what}: [{i}, {c}] = {got}, oczekiwano {v}"


# ---------------------------------------------------------------- testy
def test_interface(m, tmp):
    missing = [f for f in REQUIRED_FUNCS if not callable(getattr(m, f, None))]
    assert not missing, f"brak funkcji: {missing}"


def test_params(m, tmp):
    sid = str(getattr(m, "STUDENT_ID", ""))
    assert sid and sid != "000000", "uzupełnij STUDENT_ID swoim numerem indeksu"
    sys.path.insert(0, str(HERE))
    from parametry import get_params
    assert getattr(m, "PARAMS", None) == get_params(sid), \
        "PARAMS nie odpowiadają numerowi indeksu - wygeneruj je: python parametry.py <nr>"


def test_load_usa(m, tmp):
    df = m.load_usa(make_usa_dir(tmp))
    for c in ["name", "sex", "year", "decade", "count"]:
        assert c in df.columns, f"brak kolumny {c}"
    assert len(df) == 13, f"liczba wierszy {len(df)} != 13"
    assert list(df.index) == list(range(len(df))), "indeks powinien być 0..n-1"
    keys = list(zip(df["year"], df["sex"], -df["count"]))
    assert keys == sorted(keys), "złe sortowanie (year, sex rosnąco, count malejąco)"
    assert df["year"].tolist()[:4] == [1880] * 4 and df["decade"].tolist()[-1] == 1890
    assert as_rows(df, ["name", "sex", "count"])[:4] == [
        ("Anna", "F", 10), ("Mary", "F", 6), ("John", "M", 8), ("Anna", "M", 2)]


def test_name_stats(m, tmp):
    df = m.load_usa(make_usa_dir(tmp))
    s = m.name_stats(df)
    exp = {"unique_total": 5, "unique_F": 4, "unique_M": 3, "one_year_F": 2, "one_year_M": 1}
    for k, v in exp.items():
        assert int(s[k]) == v, f"{k} = {s[k]}, oczekiwano {v}"
    got = {int(k): int(v) for k, v in s["new_per_decade"].items()}
    assert got == {1880: 4, 1890: 1}, f"new_per_decade = {got}"


def test_frequency_rank(m, tmp):
    df = m.load_usa(make_usa_dir(tmp))[["name", "sex", "year", "count"]]
    before = df.copy()
    res = m.add_frequency_rank(df)
    assert df.equals(before), "add_frequency_rank zmodyfikowała ramkę wejściową"
    r = res.set_index(["year", "sex", "name"])
    exp = {(1880, "F", "Anna"): (0.625, 1), (1880, "M", "Anna"): (0.2, 2),
           (1881, "F", "Mary"): (0.6, 1), (1881, "F", "Anna"): (0.2, 2),
           (1881, "F", "Lu"): (0.2, 2), (1890, "F", "Kim"): (0.5, 1),
           (1890, "M", "Anna"): (3 / 13, 3)}
    for k, (f, rk) in exp.items():
        assert close(r.loc[k, "frequency"], f), f"frequency{k} = {r.loc[k, 'frequency']}, oczekiwano {f}"
        assert int(r.loc[k, "rank"]) == rk, f"rank{k} = {r.loc[k, 'rank']}, oczekiwano {rk}"


def test_unique_per_year(m, tmp):
    res = m.unique_per_year(m.load_usa(make_usa_dir(tmp)))
    check_table(res, [1880, 1881, 1890], ["F", "M"], [[2, 2], [3, 1], [2, 3]], "unique_per_year")


def test_peak_ranking(m, tmp):
    df = m.add_frequency_rank(m.load_usa(make_usa_dir(tmp)))
    r = m.peak_ranking(df, 10)
    assert list(r["F"].index) == ["Anna", "Mary", "Kim", "Lu"], f"ranking F: {list(r['F'].index)}"
    assert list(r["M"].index) == ["John", "Kim", "Anna"], f"ranking M: {list(r['M'].index)}"
    assert close(r["F"].loc["Mary", "peak"], 0.6) and int(r["F"].loc["Mary", "peak_year"]) == 1881
    assert int(r["M"].loc["Anna", "peak_year"]) == 1890
    assert list(m.peak_ranking(df, 2)["F"].index) == ["Anna", "Mary"], "nie działa ograniczenie n"


def test_coverage(m, tmp):
    df = m.load_usa(make_usa_dir(tmp))
    check_table(m.coverage(df, 0.5), [1880, 1881, 1890], ["F", "M"],
                [[1, 1], [1, 1], [1, 2]], "coverage(q=0.5)")
    check_table(m.coverage(df, 0.7), [1880, 1881, 1890], ["F", "M"],
                [[2, 1], [2, 1], [2, 2]], "coverage(q=0.7)")


def test_mean_name_length(m, tmp):
    res = m.mean_name_length(m.load_usa(make_usa_dir(tmp)))
    check_table(res, [1880, 1881, 1890], ["F", "M"],
                [[4.0, 4.0], [3.6, 4.0], [3.5, 46 / 13]], "mean_name_length")


def test_length_distribution(m, tmp):
    df = m.load_usa(make_usa_dir(tmp))
    res = m.length_distribution(df, "F", [1890, 1881])
    check_table(res, [2, 3, 4], [1890, 1881], [[0, 0.2], [0.5, 0], [0.5, 0.8]],
                "length_distribution")


def test_decade_connotation(m, tmp):
    df = m.add_frequency_rank(m.load_usa(make_usa_dir(tmp)))
    rank = m.peak_ranking(df, 10)
    res = m.decade_connotation(df, rank, 1)
    assert list(res.index) == [("Anna", 1880), ("Anna", 1890), ("Kim", 1890)], f"indeks: {list(res.index)}"
    assert int(res.loc[("Anna", 1880), "F"]) == 13 and int(res.loc[("Anna", 1890), "M"]) == 3
    assert close(res.loc[("Anna", 1880), "w_m"], 2 / 15)
    assert close(res.loc[("Anna", 1890), "dw"], 1 - 2 / 15)
    assert pd.isna(res.loc[("Kim", 1890), "dw"])
    res5 = m.decade_connotation(df, rank, 5)
    assert list(res5.index) == [("Anna", 1880), ("Kim", 1890)], "nie działa próg min_births"


def test_load_pl(m, tmp):
    df = m.load_pl(make_pl_db(tmp))
    rows = as_rows(df, ["name", "sex", "year", "count"])
    assert rows == [("ANNA", "F", 2000, 30), ("EWA", "F", 2000, 10), ("JAN", "M", 2000, 20),
                    ("ANNA", "F", 2001, 5), ("JAN", "M", 2001, 15), ("ANNA", "M", 2001, 5)], \
        f"wiersze/sortowanie: {rows}"
    assert [round(float(x), 6) for x in df["frequency"]] == [0.75, 0.25, 1.0, 1.0, 0.75, 0.25]


# ---------------------------------------------------------------- pełne uruchomienie
def run_full(script: Path) -> bool:
    print("\n--- uruchamiam cały skrypt (może potrwać) ---")
    env = dict(os.environ, MPLBACKEND="Agg")
    t0 = time.time()
    p = subprocess.run([sys.executable, script.name], cwd=script.parent, env=env,
                       capture_output=True, text=True)
    dt = time.time() - t0
    if p.returncode != 0:
        print(f"FAIL  skrypt zakończył się błędem (kod {p.returncode}):\n{p.stderr[-3000:]}")
        return False
    print(f"OK    skrypt działa, czas: {dt:.1f} s")
    ok = True
    out = script.parent / "wyniki"
    missing = [f for f in FIGURES if not (out / f).exists()]
    if missing:
        print(f"FAIL  brak wykresów: {missing}")
        ok = False
    try:
        res = json.loads((out / "results.json").read_text(encoding="utf-8"))
        for k, subkeys in RESULT_KEYS.items():
            assert isinstance(res.get(k), dict), f"brak sekcji {k}"
            miss = [s for s in subkeys if res[k].get(s) in (None, "", [])]
            assert not miss, f"{k}: brak wartości {miss}"
        assert len(res["p5"]["F"]) == 5 and len(res["p10"]["top_M"]) == 5, "p5/p10: po 5 imion"
        print("OK    results.json ma wymaganą strukturę")
    except Exception as e:  # noqa: BLE001
        print(f"FAIL  results.json: {e}")
        ok = False
    return ok


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("student", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    script = Path(sys.argv[1]).resolve()
    m = load_module(script)
    tests = [(n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)]
    passed = 0
    for name, fn in tests:
        with tempfile.TemporaryDirectory() as tmp:
            try:
                fn(m, Path(tmp))
                print(f"OK    {name}")
                passed += 1
            except Exception as e:  # noqa: BLE001
                msg = str(e) or traceback.format_exc(limit=1)
                print(f"FAIL  {name}: {type(e).__name__}: {msg}")
    print(f"\nZaliczone testy: {passed}/{len(tests)}")
    ok = passed == len(tests)
    if "--full" in sys.argv:
        ok = run_full(script) and ok
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
