# Projekt Blok 2_2025
# Eksploracyjna Analiza Danych: Skuteczność Szczepień przeciwko odrze

---

## 1. Cel projektu

Celem projektu jest eksploracyjna i statystyczna analiza danych historycznych dotyczących:
- zachorowalności na odrę,
- poziomu wyszczepialności przeciwko odrze,
- wybranych czynników społeczno-ekonomicznych,

w celu:
1. identyfikacji trendów czasowych i przestrzennych zachorowań,
2. określenia czynników sprzyjających występowaniu ognisk epidemicznych,
3. oceny związku między wyszczepialnością a odpornością populacyjną,
4. budowy modelu predykcyjnego ryzyka wystąpienia ognisk odry.

Projekt realizowany jest w duchu **eksploracyjnej analizy danych (EDA)** z wykorzystaniem metod statystycznych i elementów modelowania.

---

## 2. Kontekst epidemiologiczny

### Odra i współczynnik reprodukcji

<!-- Odra jest jedną z najbardziej zakaźnych chorób wirusowych.  
Współczynnik reprodukcji podstawowej \( R_0 \) dla odry szacowany jest na poziomie **12–18**, co oznacza bardzo wysoki potencjał epidemiczny. -->
Odra jest wysoce zakaźną chorobą wirusową. Mimo że w wielu krajach europejskich przez pewien czas uznawana była za wyeliminowaną, w ostatnim czasie obserwuje się jej nawroty, co stanowi istotne wyzwanie dla zdrowia publicznego.
Współczynnik Reprodukcji ($\text{R}_0$): Określa on średnią liczbę wtórnych zakażeń, wywołanych przez jednego chorego w populacji w pełni podatnej na zakażenie (tj. przed wprowadzeniem szczepień lub innych interwencji). Odra ma jeden z najwyższych wskaźników $\text{R}_0$, szacowany na około 12-18. Oznacza to, że jedna osoba chora może zarazić od 12 do 18 innych osób, jeśli żadna z nich nie ma odporności.



### Odporność populacyjna

W teorii krytyczny odsetek zaszczepionych (PCV – *Population Critical Value*) wymagany do uzyskania odporności populacyjnej obliczany jest jako:

\[
\text{PCV} = 1 - \frac{1}{R_0}
\]

Dla odry oznacza to poziom wyszczepialności rzędu **93–95%**.

### Kontrowersje szczepienia przeciwko odrze
Szczepionka przeciwko odrze (najczęściej w postaci skojarzonej MMR: odra, świnka, różyczka) jest wysoce skuteczna. Podawana jest w populacji dzieci i, zgodnie z aktualną wiedzą naukową, zapewnia trwałą odporność na całe życie. Ze względu na ciężki przebieg odry, zwłaszcza u małych dzieci (ryzyko powikłań takich jak zapalenie płuc, zapalenie mózgu), w większości krajów szczepienie jest kluczowym elementem przeciwdziałania zakażeniom. Wokół szczepionki MMR wciąż utrzymują się kontrowersje, które w pewnych kręgach łączą ją z występowaniem autyzmu. Choć te teorie zostały wielokrotnie obalone przez badania naukowe, ich wpływ na decyzje dotyczące szczepień w niektórych społecznościach jest zauważalny i może prowadzić do obniżenia poziomu wyszczepialności oraz wzrostu ryzyka wystąpienia ognisk odry.

---

## 3. Źródła danych

### 3.1 Dane WHO
- Zgłoszone  oraz zapadalność (na 1 000 000 mieszkańców)
- Jednostka: kraj–rok
- Zakres czasowy: **1980–2024**
- dane można pobrać ze [strony who](https://immunizationdata.who.int/global/wiise-detail-page/measles-reported-cases-and-incidence?GROUP=Countries&YEAR=) lub część informacji znajduje się w  [zasobach kursu](https://chmura.put.poznan.pl/s/7Nq8r9aceiEsdNd)

⚠️ **Uwaga metodologiczna:**  
Wartości `0` lub brak danych (`NaN`) mogą oznaczać brak raportowania, a nie rzeczywisty brak zachorowań.

---

### 3.2 Dane Banku Światowego (World Bank)

Podstawowy wskaźnik:
- `SH.IMM.MEAS` – odsetek dzieci (12–24 miesiące) zaszczepionych przeciwko odrze
do pobrania tej informacji można wykorzystać następujące zapytanie w bibliotece `wbapi`:

```python
import wbgapi as wb

indicators = {'SH.IMM.MEAS': 'Vaccination_Rate'}

wb_data = wb.data.DataFrame(list(indicators.keys()), time=range(1980, 2025), labels=True)
wb_df = wb_data.reset_index()
wb_df.rename(columns={'economy': 'Country', 'time': 'Time', **indicators}, inplace=True)
```

Przykładowe dodatkowe wskaźniki:
- PKB per capita (`NY.GDP.PCAP.CD`)
- Liczba ludności (`SP.POP.TOTL`)
- Gęstość zaludnienia (`EN.POP.DNST`)


Dopuszcza się wykorzystanie innych wskaźników lub zbiorów danych. Dla danych wbapi lista dostępnych wskaźników może być wyświetlona za pomocą komendy:
```python
wb.series.info().
```

⚠️ **Uwaga:**  
Wskaźnik `SH.IMM.MEAS` odnosi się do poziomu wyszczepienia w grupie wiekowej (kohorcie) 12–24 miesięcy. Poziom wyszczepienia całej populacji jest efektem kumulatywnym, który należy rozważać w dłuższym horyzoncie czasowym.


---

## 4. Definicje operacyjne

Na potrzeby projektu należy **jawnie zdefiniować**:

- **Ognisko epidemiczne** – np.:
  - przekroczenie określonego progu zapadalności,
  - istotny wzrost rok do roku (r/r),
  - zmienna binarna (0/1) oparta o przyjęte kryterium.

Przyjęta definicja musi być:
- jednoznaczna,
- uzasadniona,
- konsekwentnie stosowana w całej analizie.

---

## 5. Zadania projektowe

### Część I – Analiza czasowa i przestrzenna

1. Przeprowadź analizę trendów zachorowań na odrę:
   - w czasie,
     - możesz również sprawdzić czy wraz z postępującą globalizacją zmieniają się wzorce przebiegu choroby
     - czy wzrost zachorowalności ma charakter cykliczny czy też jest bardziej losowy
   - pomiędzy krajami i regionami 
     - możesz np. przeanalizować czy w danym okresie w danych regionach pojawia się więcej ognisk co może świadczyć o rozprzestrzenianiu się choroby czy też zjawiska te mają zasięg tylko lokalny.
     - czy istnieją grupy krajów o podobnych wzorcach zachorowalności (do tego celu możesz użyć np. klasteryzacji)
2. Zidentyfikuj okresy wzmożonej zachorowalności.
3. Wybierz **ok. 9 krajów** do analizy pogłębionej:
   - kraje o wysokim,
   - niskim,
   - oraz zmiennym ryzyku zachorowań.
   - możesz też wybrać inny sposób wyboru krajów, ale musi być on uzasadniony.
4. Przeanalizuj jakość danych (braki, zera, raportowanie).

---

### Część II – Analiza czynników wpływających

1. Zbadaj zależności pomiędzy:
   - zachorowalnością,
   - wyszczepialnością,
   - wskaźnikami społeczno-ekonomicznymi.
2. Zastosuj odpowiednie metody statystyczne:
   - korelacje,
   - modele regresyjne (dobór modelu musi być uzasadniony)  
3. Określ empiryczny poziom wyszczepialności ograniczający ryzyko powstawania ognisk.
4. Porównaj wynik z teoretycznym PCV.

Sugeruje się ograniczenie analizy wyłącznie krajów wybranych w Części I, ew. postawione hipotezy mogą zostać zweryfikowane na szerszym zbiorze danych.
Prócz prezentacji wyników statystycznych należy zadbać o czytelną wizualizację zależności oraz ich interpretację.

---

### Część III – Modelowanie ryzyka

1. Zbuduj model predykcyjny ryzyka wystąpienia ogniska odry.
2. Dane treningowe: **do roku 2018**.
3. Predykcja: **2019–2024**.
4. Zmienna docelowa musi być jednoznacznie zdefiniowana.
5. Podziel dane na zbiór treningowy i testowy (uzasadnij strategię).
6. Dopuszczalne jest wykorzystanie jako wejście predyktora również  informacji wskaźnikach społeczno-ekonomicznych pochodzących z lat dla których wyznaczana jest predykcja, pod warunkiem zagwarantowania braku wycieku informacji o poziomie zachorowań.

#### Ocena modelu:
- zaproponuj min. jedną metrykę jakości (np. AUC, F1, Accuracy),
- oceń zgodność predykcji z danymi rzeczywistymi,
- wskaż kraje o najwyższym i najniższym ryzyku.

---

## 6. Wymagania formalne

- Wszystkie kluczowe wnioski muszą być poparte analizą statystyczną.
- Wartości *p* należy interpretować krytycznie.
- Wymagana jest czytelna wizualizacja danych.
- Kod powinien być:
  - czytelny,
  - modularny,
  - zgodny z dobrymi praktykami (np. PEP 8).

---

## 7. Kryteria oceny

| Element | Udział |
|------|------|
| Część I – Analiza danych | 25% |
| Część II – Analiza czynników | 30% |
| Część III – Modelowanie | 25% |
| Poprawność statystyczna | 10% |
| Wnioski i struktura raportu | 10% |
| **Razem** | **100%** |

🔧 **Dodatkowo:** do 20% za jakość kodu.

---

## 8. Forma oddania

- raport w formie Notebooka Jupyter (format `.ipynb`) podzielony na sekcje odpowiadające zadaniom projektowym,
- razem z raportem należy udostępnić kod źródłowy skryptów wywoływanych przez notebook oraz wszystkie dodatkowe wykorzystane,


---
