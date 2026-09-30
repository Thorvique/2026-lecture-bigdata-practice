# Task 2 — Convergence de PageRank

Les expériences mesurent le nombre d'itérations, le temps d'exécution et le
top-10 obtenu avec différents paramètres. Les temps sont propres à cette
machine ; les nombres d'itérations décrivent le comportement de l'algorithme.

## Résultats

| # | beta | Nœuds | Tolérance | Itérations | Temps (s) | Top-10 |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.50 | 1 200 | 1e-10 | 14 | 0.013469 | p00009, p00001, p00006, p00005, p00003, p00002, p00000, p00004, p00007, p00008 |
| 2 | 0.70 | 1 200 | 1e-10 | 17 | 0.016407 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 3 | 0.85 | 1 200 | 1e-10 | 20 | 0.019454 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 4 | 0.95 | 1 200 | 1e-10 | 23 | 0.022524 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 5 | 0.99 | 1 200 | 1e-10 | 24 | 0.023337 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 6 | 0.85 | 20 000 | 1e-10 | 21 | 0.378931 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 7 | 0.95 | 20 000 | 1e-10 | 24 | 0.454025 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 8 | 0.85 | 1 200 | 1e-3 | 7 | 0.006745 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |
| 9 | 0.85 | 1 200 | 1e-6 | 12 | 0.011324 | p00009, p00001, p00006, p00005, p00003, p00002, p00004, p00000, p00007, p00008 |

## Effet de beta

Sur le graphe de 1 200 nœuds avec une tolérance de `1e-10`, le nombre
d'itérations augmente lorsque `beta` augmente : 14 itérations pour `beta=0.50`,
17 pour `0.70`, 20 pour `0.85`, 23 pour `0.95` et 24 pour `0.99`.

Le temps suit la même tendance : il passe de `0.013469 s` à `0.023337 s`.
Lorsque `beta` approche 1, le surfeur téléporte moins souvent. La correction
apportée à chaque itération est donc plus faible, ce qui ralentit la
convergence.

## Effet de la taille du graphe

Le graphe de 1 200 nœuds et celui de 20 000 nœuds permettent de comparer des
tailles séparées par plus d'un facteur 5.

Pour `beta=0.85`, le nombre d'itérations passe de 20 à 21, tandis que le temps
passe de `0.019454 s` à `0.378931 s`. Pour `beta=0.95`, il passe de 23 à 24
itérations et le temps de `0.022524 s` à `0.454025 s`.

La taille du graphe influence donc fortement le temps de chaque itération, mais
beaucoup moins le nombre d'itérations nécessaires pour converger.

## Effet de la tolérance

Avec `beta=0.85` et 1 200 nœuds :

- `tol=1e-3` : 7 itérations et `0.006745 s` ;
- `tol=1e-6` : 12 itérations et `0.011324 s` ;
- `tol=1e-10` : 20 itérations et `0.019454 s`.

Une tolérance plus stricte demande donc davantage d'itérations et davantage de
temps. Les résultats montrent le coût progressif de l'obtention de chiffres
supplémentaires de précision.

## Stabilité du top-10

Le premier changement observé est à `beta=0.70`. Entre `beta=0.50` et
`beta=0.70`, `p00000` et `p00004` échangent leur position :

- à `beta=0.50`, `p00000` est 7e et `p00004` est 8e ;
- à `beta=0.70`, `p00004` est 7e et `p00000` est 8e.

Pour les valeurs `0.70`, `0.85`, `0.95` et `0.99`, le top-10 reste identique.
Il reste également identique dans les expériences sur 20 000 nœuds et dans les
expériences avec des tolérances différentes. Le classement est donc très stable
sur ce graphe, mais le choix de `beta` peut tout de même modifier l'ordre de
pages proches dans le classement.

## Informations sur la machine

- Système d'exploitation : Microsoft Windows 11, version `10.0.26200`.
- Processeur : Intel(R) Core(TM) i9-14900HX.
- RAM physique totale détectée : 34 049 417 216 octets, soit environ 31,71 GiB.
- Version Python : 3.14.0.
- Environnement d'exécution : environnement de travail courant. La liste
  précise des autres programmes actifs pendant les mesures n'a pas été
  déterminée de manière fiable.

## Conclusions

`beta` proche de 1 ralentit la convergence. Une augmentation de la taille du
graphe augmente surtout le temps de calcul, pas le nombre d'itérations. Une
tolérance plus stricte améliore la précision au prix d'itérations
supplémentaires. Sur les expériences réalisées, le top-10 est globalement
stable et ne change pour la première fois qu'à `beta=0.70`.
