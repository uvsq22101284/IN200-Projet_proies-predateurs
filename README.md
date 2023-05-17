# IN200-Projet_proies-predateurs
Simulation de l'évolution de deux populations et leurs interactions

####################################################################

Camille LE CORRE

Lucas AUCLAIR

Nikita VERSHYNIN

LDD BI 1

####################################################################


## Présentation du projet

Ce projet a pour but de créer un système simulant la cohabitation de deux populations différentes : des proies et des prédateurs. Ces deux populations est nommé comme étant l'ensemble des animaux.
La simulation fonctionne par "tours" ; à chaque tour les animaux vieillissent et perdent de l'énergie. Ces notions seront discutées et précisées par la suite.
Il est possible de mettre en pause et de sauvegarder cette simulation afin de la charger et de la relancer ultérieurement.

Ce projet utilise la librairie tkinter pour l'interface graphique.


## Fonctionnement du projet

Les populations évoluent dans une prairie, représentée par une grille. Chaque case de la grille est associée à un tuple qui définit la nature de la case ainsi que ses paramètres associés. Ce tuple caractérisant l'identité des individus est défini selon trois indices :

- le premier indice correspond à la nature de la case (son identifiant) : 0 pour une case dite du "décor" ou de "l'environnement" (comme la prairie par exemple), 1 pour une case définissant une proie (éventuellement un lapin) et 2 pour une case définissant un prédateur (éventuellement un renard). Lorsqu'une proie et un prédateur sont sur la même case, cette indice passe à 3 avant de redevenir 2, ce qui indique que la proie a bien été mangée
- le deuxième indice correspond à l'âge et donc au temps de vie qu'il reste aux animaux de la simulation. Celui-ci est donc soit l'âge des proies, soit celui des prédateurs
- le troisième indice n'est appliqué qu'aux prédateurs. En effet, celui-ci définit l'énergie des prédateurs. Cette notion d'énergie définit la notion de satiété des prédateurs et donc caractérise leur mort par famine si l'environnement devient limité en proies. Cette énergie diminue d'une unité par tour et augmente à chaque fois qu'un prédateur mange une proie. On appelle l'énergie apportée à un prédateur par une proie : MIAM. De plus, cette énergie définit si les prédateurs peuvent se reproduire ou non. En effet, les prédateurs ne peuvent se reproduire que si leur énergie est supérieure ou égale à un certain seuil énergétique.


## Déplacement des animaux

Les proies et les prédateurs se déplacent aléatoirement dans les 8 directions sur la grille de la simulation (pour ceux se situant au milieu de la grille). Les proies ne peuvent pas aller sur une case déjà occupée par une autre proie. Cependant, si toutes les cases entourant une proie sont occupées, celle-ci ne peut pas se déplacer et reste donc fixe. Un cas typique de cette situation est si il y a une surpopulation des proies. Il en est de même pour les prédateurs.
Une proie et un prédateur peuvent se retrouver sur la même case. Dans ce cas-ci, le prédateur mange la proie.


## Apparition et reproduction des animaux sur la grille

Au début de la simulation des proies et des prédateurs apparaissent aléatoirement sur la grille.
Lorsque plusieurs individus de la même classe (proie ou prédateur) sont côte-à-côte sur la grille, un nouvel individu apparaît à proximité de ceux-ci (il faut aussi qu'une case soit libre pour la naissance du nouvel animal). Il s'agit de la reproduction et de la naissance d'un nouvel individu. Néanmoins, on rappelle qu'un prédateur doit avoir une certaine quantité d'énergie afin de se reproduire. Ce n'est pas le cas pour les proies.


## Interface graphique

Les cases de la grille prennent des couleurs différentes en fonction de leur nature. La couleur verte représente le décor de la simulation, la couleur orange représente les prédateurs (les renards) et le beige représente les proies (les lapins).

Le bouton "Sauvegarder" enregistre la configuration de la matrice correspondante à la simulation au format binaire avec la librairie pickle et le bouton "Charger" lit ce fichier et met à jour la configuration de la matrice par rapport à celle qui est enregistrée.
Le bouton "Réinitialiser" réinitialise la simulation à partir de nouvelles variables aléatoires et le bouton "Fermer" ferme la fenêtre du programme.
Quant au bouton "Démarrer/relancer la simulation", il lance le programme de la simulation et affiche la grille. Si la simulation était en pause, alors celui-ci la relance.
