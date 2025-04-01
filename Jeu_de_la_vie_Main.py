from random import choice


def generer_matrice():
    matrice = []
    for _ in range(34):
        ligne = []
        for _ in range(34):
            val = 0
            ligne.append(val)
        matrice.append(ligne)
    return matrice

def generer_matrice_vide():
    matrice = []
    for _ in range(34):
        ligne = []
        for _ in range(34):
            val = 0
            ligne.append(val)
        matrice.append(ligne)
    return matrice

def generer_matrice_aleatoire():
    matrice = []
    for _ in range(34):
        ligne = []
        for _ in range(34):
            val = choice([0, 0, 1])  # 1 chance sur 3 d'être 1
            ligne.append(val)
        matrice.append(ligne)
    return matrice

def generer_matrice_magnifique():
    matrice = generer_matrice_vide()
    matrice[15][13] = 1
    matrice[17][13] = 1
    matrice[15][14] = 1
    matrice[15][16] = 1
    matrice[15][18] = 1
    matrice[15][19] = 1
    matrice[17][19] = 1
    matrice[16][16] = 1
    matrice[18][14] = 1
    matrice[18][15] = 1
    matrice[18][16] = 1
    matrice[18][17] = 1
    matrice[18][18] = 1
    matrice[21][13] = 1
    matrice[21][14] = 1
    matrice[21][15] = 1
    matrice[21][17] = 1
    matrice[21][18] = 1
    matrice[21][19] = 1
    return matrice

def afficher_matrice(matrice):
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            print(matrice[i][j], end=" ")
        print()

def voisins_gauche(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i][j - 1] == 1:
            return 1
        else:
            return 0
    
def voisins_droite(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i][j + 1] == 1:
            return 1
        else:
            return 0

def voisins_haut(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i-1][j] == 1:
            return 1
        else:
            return 0
    
def voisins_bas(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i+1][j] == 1:
            return 1
        else:
            return 0

def voisins_haut_gauche(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i-1][j-1] == 1:
            return 1
        else:
            return 0

def voisins_haut_droite(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i-1][j+1] == 1:
            return 1
        else:
            return 0

def voisins_bas_gauche(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i+1][j-1] == 1:
            return 1
        else:
            return 0

def voisins_bas_droite(matrice, i, j):
    if i <= 1 or j <= 1:
        return 0
    if i >= 33 or j >= 33:
        return 0
    else:
        if matrice[i+1][j+1] == 1:
            return 1
        else:
            return 0

def nb_voisins(matrice, i, j):
    nb = 0
    nb += voisins_gauche(matrice, i, j)
    nb += voisins_droite(matrice, i, j)
    nb += voisins_haut(matrice, i, j)
    nb += voisins_bas(matrice, i, j)
    nb += voisins_haut_gauche(matrice, i, j)
    nb += voisins_haut_droite(matrice, i, j)
    nb += voisins_bas_gauche(matrice, i, j)
    nb += voisins_bas_droite(matrice, i, j)
    return nb

def nouvelle_generation(matrice):
    nouvelle_matrice = generer_matrice_vide()
    for i in range(30):
        for j in range(30):
            nb = nb_voisins(matrice, i+2, j+2)
            if matrice[i+2][j+2] == 1:
                if nb == 2 or nb == 3:
                    nouvelle_matrice[i+2][j+2] = 1
                else:
                    nouvelle_matrice[i+2][j+2] = 0
            else:
                if nb == 3:
                    nouvelle_matrice[i+2][j+2] = 1
                else:
                    nouvelle_matrice[i+2][j+2] = 0
    return nouvelle_matrice
            
"""matrice1 = generer_matrice()
afficher_matrice(matrice1)
print("-----------------------------------------------------------------------------------------------------------")
matrice2 = nouvelle_generation(matrice1)
afficher_matrice(matrice2)"""

