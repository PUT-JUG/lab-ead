# Lab 11 - Uczenie nienadzorowane (część 2)

## Dataset

Na zajęciach wykorzystywany będzie dość popularny zbiór zawierający informację o cechach morfologicznych 3 różnych gatunków irysów (setosa, versicolor, virginica), dla których mierzone były 4 cechy: szerokość i wysokość pręcików i płatków ![iris](_images/lab_10/iris.png).

Więcej na ten temat możesz znaleźć w [wiki](https://en.wikipedia.org/wiki/Iris_flower_data_set)

Plik z bazą można pobrać tutaj: [iris.csv](_resources/lab_10/iris.csv)

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

iris = pd.read_csv('./iris.csv')
X = iris[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y = iris['variety']
```



## Metoda K-Średnich
Metoda K średnich umożliwia nienadzorowane grupowanie elementów wielowymiarowego zbioru w klastry. W wyniku działania algorytmu K-Means dla każdego elementu zwracana jest etykieta zbioru (`estimator.labels_`), wyznaczona na podstawie minimalizacji rozproszenia elementów względem środka zbioru.

``` python
from sklearn.cluster import KMeans
from sklearn import datasets

n=3
estimator =  KMeans(n_clusters=n).fit(X)
# estimator.fit(X)
iris['cluster'] = estimator.labels_
print(iris.head)

```
Ponadto dla każdego zbioru wyznaczane są parametry:
- położenie środka zbioru (centroidu) `estimator.cluster_centers_`
- rozproszenie elementów względem środka swojego  klastra (liczona jako suma kwadratów odległości elementów od środka odpowiedniego klastra) `estimator.inertia_`

Poniższy kod wizualizuje podział na zbiory dla wybranych 2 osi (cech)
``` python
centers = pd.DataFrame(estimator.cluster_centers_, columns=['sepal.length', 'sepal.width', 'petal.length', 'petal.width'])

fig, ax = plt.subplots(figsize=(4, 4))
ax = sns.scatterplot(x='sepal.length', y='petal.length', hue='variety', style='cluster', ax=ax, data=iris)

centers.plot.scatter(x='sepal.length', y='petal.length', ax=ax, s=50, color='black')

plt.tight_layout()
plt.show()
```
Spróbuj Wygenerować serię wykresów na której wyświetlone zostaną wykresy dla pozostałych par współrzędnych

## Wyznaczanie liczby klastrów
###  Elbow method
Liczbę klastrów można oszacować na podstawie analizy rozproszenia elementów. Analizując parametr `*.inertia_` wybiera się taką wartośc przy której zmienia się szybkość spadku wartości parametru, może to sugerować pewne nasycenie.

``` python
K=range(1,10)
KM = [KMeans(k).fit(X) for k in K]
inertia = [v.inertia_ for v in KM]
plt.grid(True)
plt.xlabel('Number of clusters')
plt.ylabel('Within-cluster sum of squares')
plt.title('Elbow for KMeans clustering')

plt.plot(K, inertia, 'b*-')
```
Czy bez wiedzy na temat liczby gatunków można wskazać liczbę klastrów? Ile będzie ona wynosić?

### Metoda Silhouette
Metoda shiluete określa spójność poszczególnych klastrów, analizując odległość elementów od granicy podziału między klastrami. Wartość funkcji Silhouette wynosi 1 gdy próbka leży blisko środka 0, gdy leży na linii podziału dwóch klastrów.

Przeanalizuj [kod](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html) i dostosuj go do wykorzystania w programie. Czy jesteś w stanie dla liczebności 2,3,4,5 klastrów, które z nich mają największą spójność?

## Metoda tSNE
Jest to metoda nienadzorowana i nieparametryczna służąca do redukcji wymiarowości. Efektem jest wyodrębnienie w zredukowanej przestrzeni zbiorów, które są spójne (dla których prawdopodobieństwo przynależności elementów do danej grupy jest największe)

Przeanalizuj [przykład](https://scikit-learn.org/stable/auto_examples/manifold/plot_t_sne_perplexity.html#sphx-glr-auto-examples-manifold-plot-t-sne-perplexity-py) i spróbuj go zastosować do redukcji wymiarowości analizowanego datasetu.

1. Przeanalizuj różne wartości parametru  `perplexity` i wybierz najbardziej odpowiednią, tzn. taką która umożliwia separacje zbiorów.
2.  Używając kodu z zajęć poprzednich sprawdź jaka byłaby dokładność klasyfikacji, gdyby do klasyfikacji wykorzystać zredukowaną przestrzeń złożoną z 2 składowych wyznaczonych za pomocą algorytmu tSNE?

---
Autorzy: *Piotr Kaczmarek*  i *Jakub Tomczyński*
