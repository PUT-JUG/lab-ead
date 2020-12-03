# Lab 07 - Testowanie hipotez A/B
<!-- <-- https://www.kaggle.com/pmarcelino/comprehensive-data-exploration-with-python> -->

## Przedziały ufności
Przedział ufności pozwala na oszacowanie możliwego zakresu zmienności statystyki z założonym prawdopodobieństwem (zazwyczaj 95%).

Wykonaj następujący kod, który z populacji (`x1`) losuje 10000 próbek bootstrapowych o rozmiarze 50 elementów:
``` python
mean = 0
stdec = 0
x1 = np.random.normal(loc=mean, scale=stdev, size=50)
n_samples = 50
means = []
n_boot = 10000
for i in range(1, n_boot):
    boot = resample(x1, replace=True, n_samples=n_samples)
    means = np.append(mn, np.mean(boot))
```
Wyświetl histogram, sprawdź czy rozkład ma charakter rozkładu normalnego i oraz wartość średnią (`mn_boot`) i odchylenie standardowe (`sd_boot`).

Spróbuj teraz oszacować przedział ufności dla poziomu ufności 0.95. 
Przedział ufności danego parametru $\theta$ mieści się w zakresie ($\theta_1$;$\theta_2$) i opisany jest równaniem:

$P(\theta_1<\theta<\theta_2) = 1-\alpha = 0.95$

gdzie $\alpha$ jest nazywane poziomem istotności.

Zadanie wykonaj na 2 sposoby:
1. Zakładając poziom ufności 0.95, wektor `means` posortuj i usuń z niego po 2.5% skrajnych elementów. Następnie Odczytaj wartości pierwszego i ostatniego elementu z  zbioru, elementy te będą kresem dolnym i górnym przedziału ufności.
2. Zakładając że rozkład jest normalny zastosuj rozkład t-studenta i funkcję  [t.interval](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html)
   
   `t.interval(`$\alpha$ `, df=n_boot, loc=mean, scale=stdev)`.
   
   Zweryfikuj jaka jest różnica między przedziałem wyznaczonym w metodą nr 1.

3. Możesz również wykorzystać funkcję [`bs.bootstrap`](https://pypi.org/project/bootstrapped/), która wyznacza wartość statystyki i przedział ufności metodą próbkowania bootstrapowego. Stosując tą metodę określ jaki jest przedział ufności dla wartości średniej i odchylenia standardowego. Sprawdź, czy otrzymane przedziały zawierają teoretyczną wartość średnią, i odchylenie std, które zostały podane jako argumenty funkcji generującej przebieg.

Spróbuj teraz wygenerować i wyświetlić histogram dla rozkładu skośny:
``` python
x2 = stats.skewnorm.rvs(a=5, size=50)
```
Dla rozkładu skośnego mediana i wartość średnia nie pokrywają się. Załóżmy ze chcesz oszacować przedział ufności dla wartości średniej (wartość teoretyczna wynosi `0.78`).Zastosuje metodę 1 lub 3 oraz metodę 2. Określ przedziały ufności i porównaj różnice między metodami z tymi, które obserwowałeś dla rozkłądu normalnego. Która z tych metod jest w tym przypadku dokładniejsza?

### Prawdopodobieństwo testowe (p-value)
Prawdopodobieństwo testowe określa prawdopodobieństwo wystąpienia w populacji danej wartości statystyki  lub wartości bardziej odstającej, stąd wartość jeśli p<$\alpha$ to wartość znajduje się poza przedziałem ufności.

## Testy A/B
Celem testów jest sprawdzenie czy różnica między dwoma zbiorami A i B jest istotna. Najczęściej test ten dotyczy oceny wartości średniej i określenia czy np. czy wartość średnia zbioru B leży poza przedziałem ufności wyznaczonej dla tej statstsyki w zbiorze A.

Procedura testowania A/B polega na przyjęciu następujących Hipotez:
- hipotezy $H_0$ - nie ma różnicy między zbiorem A i B
- hipotezy alternatywnej $H_1$ jest istotna różnica między zbiorem A i B

Założony poziom istotności ($\alpha$) wpływan na zakres przedziału ufności i określa prawdopodobieństwo popełnianie błędu I rodzaju, czyli odrzucenie hipotezy $H_0$ i przyjęcie alternatywnej hipotezy $H_1$ mimo że nie jest to prawda.

1. Wygeneruj 2 tablice (A i B) o rozmiarze n=50 zmiennych losowe o rozkładzie normalnym, różniące sie wartością oczekiwaną (0 i 0.2) oraz odchyleniem standardowym (1 i 0.5). 
2.  Stosując wybraną metodę określ przedział ufności dla zmiennej A.
3.  Na poziomie istotności ($\alpha=0.05$) Zweryfikuj hipotezę że zmienna losowa A ma inną wartość średnią niż zmienna losowa B. Jeśli wartość średnia B mieści się w przedziale ufności wyznaczonym dla zmiennej A nie można odrzucić hipotezy $H_0$ Pamiętaj jednak że taka metoda działa w jedną stonę (one-way) 

Żeby dokonać weryfikacji dwukierunkowej, użyj T-Testu (dla zmiennych o rozkładzie zbliżonym do normalnego) lub testu permutacyjnego (dla zmiennych o dowolnym rozkładzie). Testy te pozwalają wyznaczyć wartość prawdopodobieństwa testowego:

1. T-Test:
``` python
from scipy import stats
n_samples = 50
rvs1 = stats.norm.rvs(loc=0,scale=1,size=n_samples0)
rvs2 = stats.norm.rvs(loc=0.2,scale=0.5,size=n_samples)
(stats, p_value) = stats.ttest_ind(rvs1, rvs2, equal_var = False)
```
2. Test permutacyjny
``` python
from mlxtend.evaluate import permutation_test

p_value = permutation_test(rvs1, rvs2,
                           method='approximate',
                           num_rounds=10000,
                           seed=0)
```
 W testach 1 i 2 otrzymaną wartość prawdopodobieństwa testowego porównaj z założony poziomem istotności, jeśli `p_value` < $\alpha$ hipotezę H0 można odrzucić i przyjąć hipotezę alternatywną.

 ## Moc testu 
 Spróbuj powtórzyć testy z poprzedniego punktu wielokrotnie (np. 1000 razy) i określ jakie jest prawdopodobieństwo tego, że wynik testu będzie poniżej założonego poziomu istotności?

 Wartość którą otrzymasz jest nazywana mocą testu i określa prawdopodobieństwo nie popełnienia błędu II rodzaju (czyli odrzucenia hipotezy $H_1$ mimo że była prawdziwa).

 Moc testu możemy również oszacować nie koniecznie tworząc nowe próbki, ale tworząc próbki bootstrapowe z aktualnie posiadanego zbioru.

 Możliwe jest również oszacowanie mocy testu/ lub określenie liczebności próby, która pozwala na uzyskanie wyniku określonej mocy.
 W tym celu należy wskazać oczekiwaną wielość efektu, która określona parametrem Cohen's d ma postać:

 `effect=`$\frac{mean(x1)-mean(x1)}{(std(x1)+std(x2))/2)}$

 Wyznacz wielkość efektu dla dla badanej poprzednio próby `rvs1` i `rvs2` oblicz moc testu: 
 ``` python
alpha =0.05
 result = analysis.solve_power(effect, power=None, nobs1=len(rvs1), ratio=1.0, alpha=alpha)
 ```

 W funkcji `solve_power` podstawiając wartość `None` pod konkretny argument i uzupełniając wartości pozostałych 2 argumentów można wyznaczyć np. liczebność próby, która powinna zostać zarejestrowana żeby uzyskać założoną moc testu przy szacowanej wielkości  efektu. Spróbuj określić jaką liczebność powinien mieć zbiór żeby uzyskać moc testu na poziomie 90%.


 # Zadanie
1. Podczas testów klinicznych szczepionki na COVID19 firma [Pfizer](https://www.pfizer.com/news/press-release/press-release-detail/pfizer-and-biontech-conclude-phase-3-study-covid-19-vaccine) wskazała, że spośród przetestowanej grupy, której podano szczepionkę 9  na 21500 zakaziło się wirusem, natomiast firma [Moderna](https://www.bbc.com/news/health-54902908) wskazała, że jej szczepionka jest skuteczniejsza ponieważ na 15000 badanych jedynie 5 osób zostało zakażonych. Spróbuj odpowiedzieć na pytania:
   - jaka jest średnia skuteczność, odchylenie standardowe rozkłądu obu szczepionek i oszacuj (metodą próbkowania bootstrapowego) jaki jest przedział ufności (stwórz wektor binarny zawierający tyle elementów ile osób brało udział w badaniach w którym 0 odpowiada osobie dla której szczepionka nie zadziałała)
   - Zweryfikuj czy prawdą jest, że jedna szczepionka jest skuteczniejsza od drugiej?
   - Wyznacz aktualną moc testu
   - Oblicz jaka powinna być populacja, przy założeniu wielkości efektu oszacowanego na posiadanej próbie, która pozwoli na stwierdzenie istotnej różnicy między szczepionkami z prawdopodobieństwem 60% 




<!-- ## Testowanie hipotez dla rozkładów wielomianowych (multinomiar distribution) -->



---
Autorzy: *Piotr Kaczmarek* i *Jakub Tomczyński*