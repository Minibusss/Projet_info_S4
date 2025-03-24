from random import randint



def generer_matrice():
    matrice = []
    for i in range(34):
        ligne = []
        for j in range(34):
            val = randint(0,1)
            ligne.append(val)
        matrice.append(ligne)
    return matrice

def generer_matrice_vide():
    matrice = []
    for i in range(34):
        ligne = []
        for j in range(34):
            val = 0
            ligne.append(val)
        matrice.append(ligne)
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

