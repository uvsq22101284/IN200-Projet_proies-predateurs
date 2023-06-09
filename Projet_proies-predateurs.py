#############################################################################
# LDD BI 1
# Lucas AUCLAIR
# Camille LE CORRE
# Nikita VERSHYNIN

# Simulation de l'évolution de deux populations et leurs interactions
#############################################################################


############################################
# Import des librairies
############################################

import tkinter as tk
import pickle
import random as rd

############################################
# Définition des constantes
############################################

HAUTEUR_CANEVAS = 500
LARGEUR_CANEVAS = 500
NB_CASES = 30


N_PRO = 30
# nombre de proies présentes avant le début de la simulation

N_PRE = 20
# nombre de prédateurs disposés aléatoirement sur la grille
# au début de la simulation

F_PRO = 0
# nombre de proies apparaissant aléatoirement à chaque tour
# constante non utilisée car nous semble inutile

A_PRO = 5
# durée de vie des proies (le même pour toutes les proies)
A_PRO_MIN = 3
# durée de vie minimum d'une proie
A_PRO_MAX = 7
# durée de vie maximum d'une proie

A_PRE = 15
# durée de vie des prédateurs
A_PRE_MIN = 12
# durée de vie minimum d'un prédateur
A_PRE_MAX = 18
# durée de vie maximum d'un prédateur

E_PRE = 10
# énergie que dispose un prédateur au début de sa vie
MIAM = 4
# énergie apportée au prédateur (E_PRE) lorsqu'il mange une proie
E_REPRO = 11
# énergie nécessaire au prédateur pour qu'il puisse se reproduire


############################################
# Définition des variables globales
############################################

global configuration_courante

est_arrete = False

global cpt_tours
cpt_tours = 0

############################################
# Définition des fonctions
############################################

############################################
# Fonctions en lien avec les widgets


def creationMatrice(n):
    """ Crée une matrice carrée de taille n contenant un tuple
    de 3 valeurs (qu'on initialise à 0)"""

    return [[(0, 0, 0)]*n for i in range(n)]


def coordonneesCase(ligne, colonne):
    """ Définie les coordonnées d'une case de la grille"""

    taille_case = LARGEUR_CANEVAS // NB_CASES

    x0 = colonne * taille_case
    y0 = ligne * taille_case
    x1 = (colonne + 1) * taille_case
    y1 = (ligne + 1) * taille_case

    liste_coordonnées = [x0, y0, x1, y1]

    return liste_coordonnées


def couleurCases(matrice):
    """ Colorie les cases de la grille en fonction de
    l'animal qui est dessus"""

    # vert : case vide (prairie)
    # beige : proie (lapin)
    # orange : prédateur (renard)

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            case = canevas.create_rectangle(
                coordonneesCase(i, j), fill="black")
            if matrice[i][j][0] == 0:
                canevas.itemconfigure(case, fill="green yellow")
            elif matrice[i][j][0] == 1:
                canevas.itemconfigure(case, fill="blanched almond")
            elif matrice[i][j][0] == 2:
                canevas.itemconfigure(case, fill="DarkOrange1")


def initialisation():
    """ Réinitialise la grille, sans animaux"""

    global cpt_tours
    global configuration_courante

    configuration_courante = creationMatrice(NB_CASES)
    couleurCases(configuration_courante)
    cpt_tours = 0


def demarrer():
    """ Démarre la simulation"""

    global est_arrete

    est_arrete = False

    tours()


def arreter():
    """Arrête la simulation ou la relance"""

    global est_arrete

    if est_arrete is False:
        est_arrete = True
    else:
        pass


def sauvegarde():
    """Sauvegarde la configuration actuelle de la grille au
    format binaire avec pickle"""

    # Méthode pickle récupérée en ligne sur la documentation correspondante

    data = configuration_courante
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)


def charger():
    """Modifie la configuration courante à partir de la
    configuration sauvegardée au format binaire avec pickle"""

    # Méthode pickle récupérée en ligne sur la documentation correspondante

    global configuration_courante
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    print(data)
    configuration_courante = data
    couleurCases(configuration_courante)


def voisinage(i, j, matrice):
    """ Créer une liste contenant le type des individus voisins d'un animal"""

    # l'ordre des voisins dans la liste est défini de gauche à droite
    # puis de haut en bas

    li = []

    if i == 0 and j == 0:
        li.append(matrice[i][j+1][0])
        li.append(matrice[i+1][j][0])
        li.append(matrice[i+1][j+1][0])
    elif i == 0 and (j == len(matrice)-1):
        li.append(matrice[i][j-1][0])
        li.append(matrice[i+1][j-1][0])
        li.append(matrice[i+1][j][0])
    elif (i == len(matrice)-1) and j == 0:
        li.append(matrice[i-1][j][0])
        li.append(matrice[i-1][j+1][0])
        li.append(matrice[i][j+1][0])
    elif (i == len(matrice)-1) and (j == len(matrice)-1):
        li.append(matrice[i-1][j-1][0])
        li.append(matrice[i-1][j][0])
        li.append(matrice[i][j-1][0])
    elif i == 0 and 0 < j < (len(matrice)-1):
        li.append(matrice[i][j-1][0])
        li.append(matrice[i][j+1][0])
        li.append(matrice[i+1][j-1][0])
        li.append(matrice[i+1][j][0])
        li.append(matrice[i+1][j+1][0])
    elif (i == len(matrice)-1) and 0 < j < (len(matrice)-1):
        li.append(matrice[i-1][j-1][0])
        li.append(matrice[i-1][j][0])
        li.append(matrice[i-1][j+1][0])
        li.append(matrice[i][j-1][0])
        li.append(matrice[i][j+1][0])
    elif (0 < i < (len(matrice)-1) and j == 0):
        li.append(matrice[i-1][j][0])
        li.append(matrice[i-1][j+1][0])
        li.append(matrice[i][j+1][0])
        li.append(matrice[i+1][j][0])
        li.append(matrice[i+1][j+1][0])
    elif 0 < i < (len(matrice)-1) and j == (len(matrice)-1):
        li.append(matrice[i-1][j-1][0])
        li.append(matrice[i-1][j][0])
        li.append(matrice[i][j-1][0])
        li.append(matrice[i+1][j-1][0])
        li.append(matrice[i+1][j][0])
    else:
        li.append(matrice[i-1][j-1][0])
        li.append(matrice[i-1][j][0])
        li.append(matrice[i-1][j+1][0])
        li.append(matrice[i][j-1][0])
        li.append(matrice[i][j+1][0])
        li.append(matrice[i+1][j-1][0])
        li.append(matrice[i+1][j][0])
        li.append(matrice[i+1][j+1][0])

    return li


def coordonneesVoisins(i, j, matrice):
    """ Créer une liste contenant les coordonnées des cases
    voisines d'une case"""

    # l'ordre des voisins dans la liste est défini de gauche à droite
    # puis de haut en bas

    li = []

    if i == 0 and j == 0:
        li.append((i, j+1))
        li.append((i+1, j))
        li.append((i+1, j+1))
    elif i == 0 and (j == len(matrice)-1):
        li.append((i, j-1))
        li.append((i+1, j-1))
        li.append((i+1, j))
    elif (i == len(matrice)-1) and j == 0:
        li.append((i-1, j))
        li.append((i-1, j+1))
        li.append((i, j+1))
    elif (i == len(matrice)-1) and (j == len(matrice)-1):
        li.append((i-1, j-1))
        li.append((i-1, j))
        li.append((i, j-1))
    elif i == 0 and 0 < j < (len(matrice)-1):
        li.append((i, j-1))
        li.append((i, j+1))
        li.append((i+1, j-1))
        li.append((i+1, j))
        li.append((i+1, j+1))
    elif (i == len(matrice)-1) and 0 < j < (len(matrice)-1):
        li.append((i-1, j-1))
        li.append((i-1, j))
        li.append((i-1, j+1))
        li.append((i, j-1))
        li.append((i, j+1))
    elif (0 < i < (len(matrice)-1) and j == 0):
        li.append((i-1, j))
        li.append((i-1, j+1))
        li.append((i, j+1))
        li.append((i+1, j))
        li.append((i+1, j+1))
    elif 0 < i < (len(matrice)-1) and j == (len(matrice)-1):
        li.append((i-1, j-1))
        li.append((i-1, j))
        li.append((i, j-1))
        li.append((i+1, j-1))
        li.append((i+1, j))
    else:
        li.append((i-1, j-1))
        li.append((i-1, j))
        li.append((i-1, j+1))
        li.append((i, j-1))
        li.append((i, j+1))
        li.append((i+1, j-1))
        li.append((i+1, j))
        li.append((i+1, j+1))

    return li


def matriceProies(matrice):
    """ Renvoie une matrice contenant la position des proies uniquement"""

    matrice_proies = [[(0, 0)]*len(matrice) for b in range(len(matrice))]

    for x in range(len(matrice_proies)):
        for y in range(len(matrice_proies)):
            if matrice[x][y][0] == 1:
                # Si c'est une proie
                matrice_proies[x][y] = (1, 0)

    return matrice_proies


def matricePredateurs(matrice):
    """ Renvoie une matrice contenant la position des prédateurs uniquement"""

    matrice_predateurs = [[(0, 0)]*len(matrice) for b in range(len(matrice))]

    for x in range(len(matrice_predateurs)):
        for y in range(len(matrice_predateurs)):
            if matrice[x][y][0] == 2:
                # Si c'est un prédateur
                matrice_predateurs[x][y] = (1, 0)

    return matrice_predateurs


def matricePredateursEnergie(matrice):
    """ Même principe que la fonction 'matricePredateurs' mais ne laisse apparaître
    uniquement les proies ayant une énergie suffisante pour se reproduire"""

    matrice_predateurs = [[(0, 0)]*len(matrice) for b in range(len(matrice))]

    for x in range(len(matrice_predateurs)):
        for y in range(len(matrice_predateurs)):
            if matrice[x][y][0] == 2:
                # Si c'est un prédateur
                if matrice[x][y][2] >= E_REPRO:
                    # S'il a une energie suffisante pour se reproduire
                    matrice_predateurs[x][y] = (1, 0, 0)

    return matrice_predateurs

############################################
# Fonctions pour la gestion des populations


def apparitionProies(matrice, n):
    """ Fait apparaître n proies aléatoirement dans la matrice"""

    cpt = 0

    while cpt != n:
        i = rd.randint(0, len(matrice)-1)
        j = rd.randint(0, len(matrice)-1)
        # On choisit au hasard une coordonnée (i,j) où une proie apparaîtra
        if matrice[i][j][0] == 0:
            # Si la case n'est pas déjà occupée
            identiteProies(matrice, i, j)
            cpt += 1

    return matrice


def apparitionPredateurs(matrice, n):
    """ Fait apparaître n prédateurs aléatoirement dans la matrice"""

    cpt = 0

    while cpt != n:
        i = rd.randint(0, len(matrice)-1)
        j = rd.randint(0, len(matrice)-1)
        # On choisit au hasard une coordonnée (i,j) où une proie apparaîtra
        if matrice[i][j][0] == 0:
            # Si la case n'est pas déjà occupée
            identitePredateurs(matrice, i, j)
            cpt += 1

    return matrice


def naissanceAleatoireProies():
    """ Fait apparaître F_PRO proies aléatoirement (à chaque début de tour)"""
    # on considère cette fonction inutile car la fonction apparitionProies
    # fait déjà apparaître un certain nombre de proies aléatoirement sur la
    # grille avant le début de la simulation. Ensuite, des nouvelles proies
    # apparaissent seulement suite à leur reproduction, car cela se
    # rapproche plus de la réalité
    pass


def identiteProies(matrice, x, y):
    """ Remplit la case de la matrice par le tuple correspondant à
    l'identité de la proie (son identifiant et son âge)"""

    # Si on veut que toutes les proies aient le même âge:
    # matrice[x][y] = (1, A_PRO, 0)

    # Si les proies ont un âge aléatoire:
    # (leur âge est compris entre A_PRO_MIN et A_PRO_MAX)
    age = rd.randint(A_PRO_MIN, A_PRO_MAX)
    matrice[x][y] = (1, age, 0)

    return


def identitePredateurs(matrice, x, y):
    """ Remplit la case de la matrice par le tuple correspondant à
    l'identité du prédateur (son identifiant, son âge et son énergie)"""

    # Si on veut que tous les prédateurs aient le même âge:
    # matrice[x][y] = (2, A_PRE, E_PRE)

    # Si les prédateurs ont un âge aléatoire:
    # (leur âge est compris entre A_PRE_MIN et A_PRE_MAX)
    age = rd.randint(A_PRE_MIN, A_PRE_MAX)
    matrice[x][y] = (2, age, E_PRE)

    return


def ageProies(matrice):
    """ Prend en argument la matrice et diminue de 1 l'âge
    de toutes les proies"""

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j][0] == 1:
                # si c'est une proie
                matrice[i][j] = (matrice[i][j][0], (
                    matrice[i][j][1] - 1), matrice[i][j][2])
                # son âge diminue de 1


def ageEnergiePredateurs(matrice):
    """ Prend en argument la matrice et diminue de 1 l'âge
    et l'énergie de tous les prédateurs"""

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j][0] == 2:
                # si c'est un prédateur
                matrice[i][j] = (matrice[i][j][0], (
                    matrice[i][j][1] - 1), matrice[i][j][2])
                # son âge diminue de 1
                matrice[i][j] = (matrice[i][j][0], (
                    matrice[i][j][1]), (matrice[i][j][2]-1))
                # son énergie diminue de 1


def deplacementProies(matrice):
    """ Fait bouger toutes les proies"""

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j][0] == 1:
                # Si c'est une proie
                voisins = voisinage(i, j, matrice)
                coord_voisins = coordonneesVoisins(i, j, matrice)
                if (0 in voisins) or (2 in voisins):
                    while matrice[i][j][0] != 0:
                        # Tant que l'animal n'a pas bougé
                        k = rd.randint(0, (len(voisins)-1))
                        if voisins[k] == 0:
                            i_arrivee = coord_voisins[k][0]
                            j_arrivee = coord_voisins[k][1]
                            matrice[i_arrivee][j_arrivee] = matrice[i][j]
                            matrice[i][j] = (0, 0, 0)
                        elif voisins[k] == 2:
                            i_arrivee = coord_voisins[k][0]
                            j_arrivee = coord_voisins[k][1]
                            matrice[i_arrivee][j_arrivee] = (
                                3, (matrice[i_arrivee][j_arrivee][1]), (
                                    matrice[i_arrivee][j_arrivee][2]))
                            matrice[i][j] = (0, 0, 0)

    return matrice


def deplacementPredateurs(matrice):
    """ Fait bouger tous les prédateurs"""

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j][0] == 2:
                # Si c'est un prédateur
                voisins = voisinage(i, j, matrice)
                coord_voisins = coordonneesVoisins(i, j, matrice)
                if (0 in voisins) or (2 in voisins):
                    while matrice[i][j][0] != 0:
                        # Tant que l'animal n'a pas bougé
                        k = rd.randint(0, (len(voisins)-1))
                        if voisins[k] == 0:
                            i_arrivee = coord_voisins[k][0]
                            j_arrivee = coord_voisins[k][1]
                            matrice[i_arrivee][j_arrivee] = matrice[i][j]
                            matrice[i][j] = (0, 0, 0)
                        elif voisins[k] == 1:
                            i_arrivee = coord_voisins[k][0]
                            j_arrivee = coord_voisins[k][1]
                            matrice[i_arrivee][j_arrivee] = (
                                3, (matrice[i][j][1]), matrice[i][j][2])
                            matrice[i][j] = (0, 0, 0)

    return matrice


def reproductionProies(matrice):
    """ Si 2 proies sont à côté, alors elles se reproduisent
    (on décide que les proies ne peuvent se reproduire au
    maximum qu'une seule fois par tour)"""

    mat_proies = matriceProies(matrice)

    # On parcourt notre matrice contenant les informations
    # des positions des proies puis l'on regarde si une proie
    # est à coté d'une autre ; si c'est le cas, elles se reproduisent

    for i in range(len(mat_proies)):
        for j in range(len(mat_proies)):
            if mat_proies[i][j] == (1, 0):
                # Si c'est une proie
                voisins = voisinage(i, j, mat_proies)
                voisins_vide = voisinage(i, j, matrice)
                if (1 in voisins) and (0 in voisins_vide):
                    # Si la proie est à côté d'une autre proie
                    # et qu'il y a une case vide pour la naissance
                    verif_naissance = 0
                    while mat_proies[i][j] == (1, 0):
                        # Tant que la proie ne s'est pas reproduit
                        h = rd.randint(0, (len(voisins)-1))
                        if voisins[h] == 1:
                            # Si un voisin pris au hasard est une proie,
                            # il y a reproduction
                            mat_proies[i][j] = (0, 0)
                            # La proie ne peut plus se reproduire
                            # pendant ce tour
                            coord_pro = coordonneesVoisins(i, j, matrice)
                            mat_proies[coord_pro[h][0]][coord_pro[h][1]] = (
                                0, 0)
                            while verif_naissance == 0:
                                # Tant qu'il n'y a pas eu la naissance
                                k = rd.randint(0, (len(voisins_vide)-1))
                                if voisins_vide[k] == 0:
                                    # Si la case choisie au hasard est vide
                                    identiteProies(
                                        matrice, coord_pro[k][0], (
                                            coord_pro[k][1]))
                                    # matrice[coord_pro[k][0]][coord_pro[k][1]]
                                    # = (1, A_PRO)
                                    verif_naissance = 1

    return matrice


def reproductionPredateurs(matrice):
    """ Si 2 prédateurs sont à côté et que leur énergie est
    supérieure à l'énergie nécessaire pour la reproduction
    (E_repro), alors ils se reproduisent"""

    matrice_pred = matricePredateursEnergie(matrice)

    # On parcourt notre matrice contenant les informations des
    # positions des proies puis l'on regarde si une proie est à
    # coté d'une autre ; si c'est le cas, elles se reproduisent

    for i in range(len(matrice_pred)):
        for j in range(len(matrice_pred)):
            if matrice_pred[i][j] == (1, 0, 0):
                # Si c'est un prédateur
                voisins = voisinage(i, j, matrice_pred)
                voisins_vide = voisinage(i, j, matrice)
                if (1 in voisins) and (0 in voisins_vide):
                    # Si le prédateur est à côté d'un autre prédateur
                    # et qu'il y a une case vide pour la naissance
                    verif_naissance = 0
                    while matrice_pred[i][j] == (1, 0, 0):
                        # Tant que le prédateur ne s'est pas reproduit
                        h = rd.randint(0, (len(voisins)-1))
                        if voisins[h] == 1:
                            # Si un voisin pris au hasard est aussi un
                            # prédateur, il y a reproduction
                            matrice_pred[i][j] = (0, 0, 0)
                            # Le prédateur ne peut plus se
                            # reproduire pendant ce tour
                            coord_pro = coordonneesVoisins(i, j, matrice)
                            matrice_pred[coord_pro[h][0]][coord_pro[h][1]] = (
                                0, 0, 0)
                            while verif_naissance == 0:
                                # Tant qu'il n'y a pas eu la naissance
                                k = rd.randint(0, (len(voisins_vide)-1))
                                if voisins_vide[k] == 0:
                                    # Si la case choisie au hasard est vide
                                    identitePredateurs(
                                        matrice, coord_pro[k][0], (
                                            coord_pro[k][1]))
                                    verif_naissance = 1

    return matrice


def predation(matrice):
    """ Si une proie et un prédateur sont sur la même case,
    alors la proie meure et le prédateur gagne MIAM"""

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j][0] == 3:
                # Si une proie et un prédateur se
                # retrouvent sur la même case
                matrice[i][j] = (2, matrice[i][j][1], (
                    matrice[i][j][2] + MIAM))

    return matrice


def mortProies(matrice):
    """ Prend en argument une matrice, vérifie la durée de vie
    restante de toutes les proies, si elle est égale à 0, alors
    elle meurt donc l'identité de la case devient un tuple de 0"""

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j][0] == 1 and matrice[i][j][1] == 0:
                # si c'est une proie et
                # qu'elle est trop âgée
                matrice[i][j] = (0, 0, 0)
                # devient une case du décor

    return matrice


def mortPrédateurs(matrice):
    """ Prend en argument une matrice, vérifie la durée de vie
    restante et l'énergie E_PRE de tous les prédateurs, si au
    moins l'une des deux est égale à 0, alors il meurt donc
    l'identité de la case devient un tuple de 0"""

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j][0] == 2:
                # s'il s'agit d'un prédateur
                if matrice[i][j][1] == 0:
                    # s'il est trop âgé
                    matrice[i][j] = (0, 0, 0)
                    # devient une case du décor
                elif matrice[i][j][2] == 0:
                    # s'il n'a plus d'énergie
                    matrice[i][j] = (0, 0, 0)
                    # devient une case du décor

    return matrice


def tours():
    """Fonction qui gère les tours et les conditions associées
    à ceux-ci en appelant toutes les fonctions qui gèrent les
    variations d'états liés aux tours"""

    global est_arrete
    global cpt_tours
    global configuration_courante

    if est_arrete is False:
        if cpt_tours == 0:
            apparitionProies(configuration_courante, N_PRO)
            apparitionPredateurs(configuration_courante, N_PRE)

        deplacementProies(configuration_courante)
        predation(configuration_courante)
        deplacementPredateurs(configuration_courante)
        predation(configuration_courante)
        # on appelle la fonction 2 fois car on considère
        # que dès qu'un prédateur se trouve sur la même
        # case qu'une proie, il la mange
        reproductionProies(configuration_courante)
        reproductionPredateurs(configuration_courante)
        # pas besoin de rappeler la fonction prédation car
        # les naissances se font sur des cases vides
        ageProies(configuration_courante)
        ageEnergiePredateurs(configuration_courante)

        mortProies(configuration_courante)
        mortPrédateurs(configuration_courante)

        couleurCases(configuration_courante)

        cpt_tours += 1
        canevas.after(30, tours)
        return


############################################
# Boucle principale
############################################


racine = tk.Tk()
racine.title("Simulation d'un système proies/prédateurs")

configuration_courante = creationMatrice(NB_CASES)

############################################
# Création des widgets


canevas = tk.Canvas(
    racine, height=HAUTEUR_CANEVAS, width=LARGEUR_CANEVAS, bg='white')
initialisation()

bouton_reinitialiser = tk.Button(
    racine, text="Réinitialiser", command=initialisation)
bouton_demarrer = tk.Button(
    racine, text="Démarrer/relancer la simulation", command=demarrer)
bouton_arreter = tk.Button(
    racine, text="Mettre en pause la simulation", command=arreter)
bouton_sauvegarder = tk.Button(
    racine, text="Sauvegarder", command=sauvegarde)
bouton_charger = tk.Button(
    racine, text="Charger", command=charger)
bouton_fermer_fenetre = tk.Button(
    racine, text="Fermer", command=racine.destroy)


############################################
# Placement des widgets

canevas.grid(column=1, row=0, rowspan=6)

bouton_reinitialiser.grid(column=0, row=0)
bouton_demarrer.grid(column=0, row=1)
bouton_arreter.grid(column=0, row=2)
bouton_sauvegarder.grid(column=0, row=3)
bouton_charger.grid(column=0, row=4)
bouton_fermer_fenetre.grid(column=0, row=5)


racine.mainloop()
