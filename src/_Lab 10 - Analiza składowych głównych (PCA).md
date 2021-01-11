# Lab 10 - Wybór cech i redukcja wymiarowości zbiorów (część 1)

## Dataset
Na zajęciach wykorzystywany będzie dość popularny zbiór zawierający informację o cechach morfologicznych 3 różnych gatunków irysów (setosa, versicolor, virginica), dla których mierzone były 4 cechy: szerokość i wysokość pręcików i płatków ![obraz](../src/_images/lab_10/iris.png).
Więcej na ten temat możesz znaleźć w [wiki](https://en.wikipedia.org/wiki/Iris_flower_data_set) Plik z bazą można pobrać [iris.csv](../src/_resources/lab_10/iris.csv)
``` python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

iris = pd.read_csv('./iris.csv')
sns.pairplot(iris, hue="variety")
```
Przeanalizuj strukturę zbioru danych oraz `pairplot`.
Jakie wnioski/spostrzeżenia dotyczące rozkładu danych możesz wskazać

## Macierz korelacji
Wyznacz macierz korelacji i przeanalizuj zależności między poszczególnymi parametrami. Określ, które z nich są najsilniej/najsłabiej ze sobą związane i umożliwiają najlepszą separację gatunków? 
``` python
ax = sns.heatmap(iris.corr(), annot=True)
```

Czy jesteś w stanie, bazując na macierzy korelacji i wykresach par cech, wskazać cechy, które warto byłoby wybrać do klasyfikacji (którą są liniowo separowalne? 
Spróbuj wybrać 1 i 2 cechy i porównaj wynik klasyfikacji z wynikiem uzyskanym dla wszystkich cech. 
W celu oceny możesz użyć następującego kodu wykorzystującego do klasyfikacji liniową analizę dyskryminacyjną (LDA):
``` python

from numpy import mean
from numpy import std

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

model = LinearDiscriminantAnalysis()

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

scores = cross_val_score(model, iris[['sepal.length','sepal.width','petal.length','petal.width']], iris['variety'], scoring='accuracy', cv=cv, n_jobs=-1)

print('Mean Accuracy: %.3f (%.3f)' % (mean(scores), std(scores)))
```
Jaka jest różnica? Czy jest możliwe że dla zbioru złożonego z jednej cechy uzyskamy większą dokładność niż dla zbioru złożonego z 2 cech? Spróbuj uzasadnić zaobserwowane efekty?


## Analiza składowych głównych (PCA)

Dokonaj przekształcenia zbioru danych metodą analizy składowych głównych. Więcej na ten temat możesz znaleźć w materiałach z wykładu.
Wyznaczenie skłądowych głównych polega na wyznaczeniu macierzy rotacji w przestrzeni cech, która maksymalizuje wariancję wzdłuż kolejnych składowych.

Transformację PCA możesz wykonać realizując następujący kod:
``` python

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

scaler = StandardScaler()
X=scaler.fit_transform(X)

pca = PCA()
X_pca = pca.fit_transform(X)

iris_pca = pd.DataFrame(data=X_pca)
iris_pca['variety'] = iris['variety']
```

1. Spróbuj zaobserwować co zmieniło się w macierzy korelacji oraz z wykresie par cech?
2. Przeanalizuj zmienną `pca.components_` zawierającą macierz rotacji, pamiętaj że po wyznaczeniu parametrów transformacji PCA, możesz ją zrealizować mnożąc macierz cech przez macierz rotacji: `np.transpose(pca.components_@np.transpose(X))` lub wywołując metodę `pca.fit(X)`
3. Przeanalizuj zdolność wyjaśniającą każdej ze składowych: `pca.explained_variance_ratio_` ile procent zbioru można odtworzyć jeśli wykorzystamy tylko 2 cechy?
4. Czy wybór cech do klasyfikacji w oparciu o zdolność wyjaśniającą w tym przypadku jest bardziej skuteczny niż wybór cech do klasyfikacji na podstawie analizy eksploracyjnej? Spróbuj uzasadnić swoją obserwację?

## Zastosowanie analizy PCA do wyznaczania macierzy synergii manipulatora



   




---
Autorzy: *Piotr Kaczmarek*  i *Jakub Tomczyński*
