# Task 1 — PageRank et ses deux problèmes

Sans téléportation, le rang d'un dead end n'est transmis à aucun autre nœud et
disparaît progressivement du graphe ; sur le test, la somme finale est
`0.0000`. Dans la version correcte, nous redistribuons uniformément cette masse
sur tous les nœuds, ce qui conserve la somme à `1.000000`.

La téléportation empêche aussi un spider trap d'absorber tout le rang : le
surfeur peut quitter le piège et rejoindre n'importe quel nœud. `beta` est la
probabilité de suivre un lien ; avec `1 - beta`, le surfeur se téléporte vers un
nœud choisi uniformément. Les sept vérifications de Task 1 sont passées.

# Task 2 — Convergence

Sur 1 200 nœuds avec `tol=1e-10`, le nombre d'itérations augmente de 14 à
`beta=0.50` jusqu'à 24 à `beta=0.99`, car la téléportation devient moins
fréquente et ralentit la convergence. Le temps augmente également, de
`0.013469 s` à `0.023337 s`.

Passer de 1 200 à 20 000 nœuds augmente fortement le temps (`0.019454 s` à
`0.378931 s` pour `beta=0.85`), mais presque pas le nombre d'itérations (20 à
21) ; pour `beta=0.95`, il passe de 23 à 24. Avec `beta=0.85`, les tolérances
`1e-3`, `1e-6` et `1e-10` demandent respectivement 7, 12 et 20 itérations.
Le premier changement du top-10 est observé à `beta=0.70`, lorsque `p00004`
et `p00000` échangent leur position ; le classement reste ensuite stable dans
les expériences réalisées.

# Task 3 — Sparse PageRank

La matrice dense `n×n` est remplacée par la liste d'adjacence déjà fournie et
deux vecteurs de rang, contenant les rangs anciens et nouveaux. Le benchmark
mesure `1 440 000` flottants pour la version dense contre `2 400` pour la
version sparse, soit `600×` moins, avec une différence maximale de seulement
`1.18e-15` par nœud.

La téléportation ne nécessite pas de matrice dense : chaque nœud reçoit
simplement le même scalaire `(1-beta)/n`, ajouté pendant la construction du
nouveau vecteur, en `O(n)`. La version sparse est `44.3×` plus rapide que la
version dense et a obtenu le niveau `strong` du benchmark.
