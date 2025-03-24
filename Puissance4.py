from tkinter import *

# Paramètre
Largeur = 1000
Hauteur = 750

# Fenetre
Puissance4 = Tk()
Puissance4.iconbitmap("logo.ico")
Puissance4.title("Puissance4")
Puissance4.minsize(Largeur,Hauteur)
Puissance4.maxsize(Largeur,Hauteur)
Puissance4.config(background="#2045F4")
# Matrice de Jeu :
MatriceP4 = [0] * 6
for i in range(6) :
    MatriceP4[i] = [0]*7
for m in range(6):
    print(MatriceP4[m])
MatriceP4_J = [0] * 6
for i in range(6) :
    MatriceP4_J[i] = [0]*7

# Mise en place du clic
def ClicCase(event) :
    Coupsjoués = 0
    for A in range(6) :
        for B in range(7) :
            if MatriceP4[A][B] != MatriceP4_J[A][B] :
                Coupsjoués +=1
    print("Coup Joués :", Coupsjoués)
    i_c = 0
    j_c = 0
    x_c = event.x
    y_c = event.y
    for a in range(6) : # Check de la case pour la matrice
        for b in range(7) :
            if b*(Largeur/7) < x_c < (b+1)*(Largeur/7) and a*(Hauteur/6) < y_c < (a+1)*(Hauteur/6) :
                i_c = b
                j_c = a
    
    if MatriceP4[j_c][i_c] != 0 :
        print("Place déja prise")
    else : #Case libre, calcul du joueur 
        if Coupsjoués%2 == 0 and MatriceP4[j_c][i_c] == 0 :
            CercleJoué = Jeu.create_oval((i_c*(Largeur)/7)+25, (j_c*(Hauteur)/6)+18.75,((i_c+1)*(Largeur)/7)-25,((j_c+1)*(Hauteur)/6)-18.75, outline="black", fill = "Red")
            MatriceP4[j_c][i_c] = 1
            print("-------------------------------------------------------------------------")
            for m in range(6):
                print(MatriceP4[m])
        if Coupsjoués%2 == 1 and MatriceP4[j_c][i_c] == 0:
            CercleJoué = Jeu.create_oval((i_c*(Largeur)/7)+25, (j_c*(Hauteur)/6)+18.75,((i_c+1)*(Largeur)/7)-25,((j_c+1)*(Hauteur)/6)-18.75, outline="black", fill = "Yellow")
            MatriceP4[j_c][i_c] = 2
            print("-------------------------------------------------------------------------")
            for m in range(6):
                print(MatriceP4[m])
    
Puissance4.bind('<Button-1>', ClicCase)
# Zone de jeu 
Jeu = Canvas(Puissance4, width = Largeur, height = Hauteur, bg="#2045F4")
for i in range(6) : #ligne horizontale
    LigneH = Jeu.create_line(0, i*(Hauteur/6),Largeur, i*(Hauteur/6))
for i in range(7) : #ligne verticale
    LigneV = Jeu.create_line(i*(Largeur/7), 0, i*(Largeur/7),Hauteur)
for a in range(6) :
    for b in range(7) : # Cases
        CercleJeu = Jeu.create_oval((b*(Largeur)/7)+25, (a*(Hauteur)/6)+18.75,((b+1)*(Largeur)/7)-25,((a+1)*(Hauteur)/6)-18.75, outline="black", fill = "white")
# Mise en place des éléments
Jeu.place(x = 0, y =0)
Puissance4.mainloop()