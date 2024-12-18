# Lab 07 - Testowanie hipotez A/B
<!-- <-- https://www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python> -->

## Przedziały ufności
Przedział ufności pozwala na oszacowanie możliwego zakresu zmienności statystyki z założonym prawdopodobieństwem (zazwyczaj 95%).

Wykonaj następujący kod, który z populacji (`x1`) losuje 10000 próbek bootstrapowych o rozmiarze 50 elementów:
```python
x1_mean = 0
x1_stddev = 1
x1 = np.random.normal(loc=x1_mean, scale=x1_stddev, size=50)
n_samples = 50
means = []
n_boot = 10000
for i in range(1, n_boot):
    boot = sklearn.utils.resample(x1, replace=True, n_samples=n_samples)
    means.append(np.mean(boot))
```
Wyświetl histogram, sprawdź czy rozkład ma charakter rozkładu normalnego oraz wyznacz wartość średnią (`mn_boot`) i odchylenie standardowe (`sd_boot`).

Spróbuj teraz oszacować przedział ufności dla poziomu ufności 0.95. 
Przedział ufności danego parametru *θ* mieści się w zakresie (*θ<sub>1</sub>*; *θ<sub>2</sub>*) i opisany jest równaniem:

![przedzial_ufnosci](_images/lab_07/przedzial_ufnosci.svg)

gdzie *ɑ* jest nazywane poziomem istotności.

Zadanie wykonaj na 2 sposoby:
1. Zakładając poziom ufności 0.95, posortuj wektor `means` i usuń z niego po 2.5% skrajnych elementów. Następnie Odczytaj wartości pierwszego i ostatniego elementu z  zbioru, elementy te będą kresem dolnym i górnym przedziału ufności.
2. Zakładając, że rozkład jest normalny zastosuj rozkład t-Studenta i funkcję  [t.interval](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)
   
```python
from scipy import stats

SE = np.std(x1) / np.sqrt(len(x1)) #błąd standardowy dla rozkładu normlanego
t_student_interval = stats.t.interval(1 - alpha, df=n_samples - 1, loc=np.mean(x1), scale=SE)  # uwaga! pierwszy parametr oznacza poziom ufności 
```
   
Zweryfikuj jaka jest różnica między przedziałem wyznaczonym metodą nr 1 oraz jaka jest różnica między błędem standardowym (`SE`) a wariancją średniej wyznaczonej metodą bootstrapu (`st_boot`).

3. Możesz również wykorzystać funkcję [`bs.bootstrap`](https://pypi.org/project/bootstrapped/), która wyznacza wartość statystyki i przedział ufności metodą próbkowania bootstrapowego. Stosując tą metodę określ jaki jest przedział ufności dla wartości średniej i odchylenia standardowego. Sprawdź, czy otrzymane przedziały zawierają teoretyczną wartość średnią i odchylenie standardowe, które zostały podane jako argumenty funkcji generującej przebieg:


```python
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats


bs_mean_interval = bs.bootstrap(x1, stat_func=bs_stats.mean)
bs_std_interval = bs.bootstrap(x1, stat_func=bs_stats.std)
```

Spróbuj teraz wygenerować i wyświetlić histogram dla rozkładu skośnego:

```python
x2 = stats.skewnorm.rvs(a=5, size=50)
```

Dla rozkładu skośnego mediana i wartość średnia nie pokrywają się. Załóżmy, że chcesz oszacować przedział ufności dla wartości średniej (wartość teoretyczna wynosi `0.78`). Zastosuj metodę 1 lub 3 oraz metodę 2. Określ przedziały ufności i porównaj różnice między metodami z tymi, które obserwowałeś dla rozkładu normalnego. Która z tych metod jest w tym przypadku dokładniejsza?

### Prawdopodobieństwo testowe (p-value)

Prawdopodobieństwo testowe określa prawdopodobieństwo wystąpienia w populacji danej wartości statystyki lub wartości bardziej odstającej, stąd wartość jeśli *p* < *ɑ*, to wartość znajduje się poza przedziałem ufności.

## Testy A/B

Celem testów jest sprawdzenie czy różnica między dwoma zbiorami A i B jest istotna. Najczęściej test ten dotyczy oceny wartości średniej i określenia czy np. czy wartość średnia zbioru B leży poza przedziałem ufności wyznaczonej dla tej statystyki w zbiorze A.

Procedura testowania A/B polega na przyjęciu następujących hipotez:
- hipotezy *H_<sub>0</sub>* - nie ma różnicy między zbiorem A i B
- hipotezy alternatywnej *H_<sub>1</sub>* jest istotna różnica między zbiorem A i B

Założony poziom istotności (*ɑ*) wpływa na zakres przedziału ufności i określa prawdopodobieństwo popełnianie błędu I rodzaju, czyli odrzucenie hipotezy *H_<sub>0</sub>* i przyjęcie alternatywnej hipotezy *H_<sub>1</sub>* mimo że nie jest to prawda.

1. Wygeneruj 2 tablice losowe (A i B) o rozmiarze n=50 zmiennych i rozkładzie normalnym, różniące sie wartością oczekiwaną (odpowiednio 0 i 0.2) oraz odchyleniem standardowym (odpowiednio 1 i 0.5). 
2. Stosując wybraną metodę określ przedział ufności dla zmiennej A.
3. Na poziomie istotności (*ɑ*=0.05) zweryfikuj hipotezę, że zmienna losowa A ma inną wartość średnią niż zmienna losowa B. Jeśli wartość średnia B mieści się w przedziale ufności wyznaczonym dla zmiennej A, nie można odrzucić hipotezy *H_<sub>0</sub>*. Pamiętaj jednak, że taka metoda działa w jedną stonę (one-way).

Żeby dokonać weryfikacji dwukierunkowej, użyj T-Testu (dla zmiennych o rozkładzie zbliżonym do normalnego) lub testu permutacyjnego (dla zmiennych o dowolnym rozkładzie). Testy te pozwalają wyznaczyć wartość prawdopodobieństwa testowego:

1. T-Test:
```python
from scipy import stats


n_samples = 50
rvs1 = stats.norm.rvs(loc=0, scale=1, size=n_samples)
rvs2 = stats.norm.rvs(loc=0.2, scale=0.5, size=n_samples)
(stats, p_value) = stats.ttest_ind(rvs1, rvs2, equal_var = False)
```

2. Test permutacyjny
```python
# from mlxtend.evaluate import permutation_test
from scipy.stats import permutation_test
def statistic(x, y, axis=0):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)

p_value = permutation_test((rvs1, rvs2), statistic,
                           n_resamples=np.inf, alternative='two-sided')
```
 W testach 1 i 2 otrzymaną wartość prawdopodobieństwa testowego porównaj z założony poziomem istotności, jeśli `p_value` < *ɑ* hipotezę *H<sub>0</sub>* można odrzucić i przyjąć hipotezę alternatywną.

 ## Moc testu 
 
 Spróbuj powtórzyć testy z poprzedniego punktu wielokrotnie (np. 1000 razy) i określ jakie jest prawdopodobieństwo tego, że wynik testu będzie poniżej założonego poziomu istotności?

 Wartość którą otrzymasz jest nazywana mocą testu i określa prawdopodobieństwo nie popełnienia błędu II rodzaju (czyli odrzucenia hipotezy *H<sub>1</sub>* mimo że była prawdziwa).

 Moc testu możemy również oszacować nie koniecznie tworząc nowe próbki, ale tworząc próbki bootstrapowe z aktualnie posiadanego zbioru.

 Możliwe jest również oszacowanie mocy testu lub określenie liczebności próby, która pozwala na uzyskanie wyniku określonej mocy.
 W tym celu należy wskazać oczekiwaną wielość efektu, która określona parametrem Cohen's *d* ma postać:

![effect_size](_images/lab_07/effect_size.svg)

 Wyznacz wielkość efektu dla dla badanej poprzednio próby `rvs1` i `rvs2` oblicz moc testu: 
 
 ```python
from statsmodels.stats.power import TTestIndPower
 
 
analysis = TTestIndPower()
result = analysis.solve_power(effect, power=None, nobs1=len(rvs1), ratio=1.0, alpha=alpha)
 ```

 W funkcji `solve_power` podstawiając wartość `None` pod wybrany argument i uzupełniając wartości pozostałych 2 argumentów można wyznaczyć np. liczebność próby, która powinna zostać zarejestrowana żeby uzyskać założoną moc testu przy szacowanej wielkości  efektu. Spróbuj określić jaką liczebność powinien mieć zbiór żeby uzyskać moc testu na poziomie 90%.


 # Zadanie

1. Podczas testów klinicznych szczepionki na COVID19 firma [Pfizer](https://www.pfizer.com/news/press-release/press-release-detail/pfizer-and-biontech-conclude-phase-3-study-covid-19-vaccine) wskazała, że spośród przetestowanej grupy, której podano szczepionkę 9 na 21500 zakaziło się wirusem, natomiast firma [Moderna](https://www.bbc.com/news/health-54902908) wskazała, że jej szczepionka jest skuteczniejsza ponieważ na 15000 badanych jedynie 5 osób zostało zakażonych. Spróbuj odpowiedzieć na pytania:
   
   - Jaka jest średnia skuteczność, odchylenie standardowe rozkładu obu szczepionek i oszacuj (metodą próbkowania bootstrapowego) jaki jest przedział ufności (stwórz wektor binarny zawierający tyle elementów ile osób brało udział w badaniach w którym 0 odpowiada osobie, dla której szczepionka nie zadziałała)
   - Zweryfikuj czy prawdą jest, że jedna szczepionka jest skuteczniejsza od drugiej?
   - Wyznacz aktualną moc testu
   - Oblicz jaka powinna być populacja, przy założeniu wielkości efektu oszacowanego na posiadanej próbie, która pozwoli na stwierdzenie istotnej różnicy między szczepionkami z prawdopodobieństwem 60% 




<!-- ## Testowanie hipotez dla rozkładów wielomianowych (multinomiar distribution) -->


---
Autorzy: *Piotr Kaczmarek* i *Jakub Tomczyński*
