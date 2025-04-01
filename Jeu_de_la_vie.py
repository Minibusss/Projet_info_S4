import tkinter as tk
import Jeu_de_la_vie_Main as module

def affichage():
    global buttons, matrice, fenetre, jeu_en_cours
    fenetre = tk.Tk()
    fenetre.title("Jeu de la vie")
    fenetre.geometry("1000x900")  
    fenetre.iconbitmap("logo.ico")
    fenetre.config(background='#FFFFFF')

    jeu_en_cours = False  # Variable pour gérer le démarrage et l'arrêt du jeu

    frame_boutons = tk.Frame(fenetre, bg="white")
    frame_boutons.pack(side=tk.TOP, pady=10)

    frame = tk.Frame(fenetre, bg='#FFFFFF', bd=1, relief=tk.SUNKEN)
    frame.pack(expand=tk.YES)

    matrice = module.generer_matrice_vide()  # Doit être une matrice 34x34

    monBouton1 = tk.Button(frame_boutons, text="Lancer le jeu", bg="white", command=lancer_jeu)
    monBouton2 = tk.Button(frame_boutons, text="Pause", bg="white", command=pause)
    monBouton3 = tk.Button(frame_boutons, text="remplissage Aléatoire", bg="white", command=aleatoire)
    monBouton4 = tk.Button(frame_boutons, text="Le Bonheur visuel", bg="white", command=bonheur_visuel)
    monBouton5 = tk.Button(frame_boutons, text="Quitter", bg="white", command=fenetre.quit)
    monBouton6 = tk.Button(frame_boutons, text="effacer", bg="white", command=effacer)
    
    

    monBouton1.pack(side=tk.LEFT, padx=5)
    monBouton2.pack(side=tk.LEFT, padx=5)
    monBouton3.pack(side=tk.LEFT, padx=5)
    monBouton4.pack(side=tk.LEFT, padx=5)
    monBouton5.pack(side=tk.LEFT, padx=5)
    monBouton6.pack(side=tk.LEFT, padx=5)

    buttons = []

    for i in range(34):  
        row = []
        for j in range(34):  
            # Désactiver les boutons des bords
            if i < 2 or i >= 32 or j < 2 or j >= 32:
                btn = tk.Button(frame, width=2, height=1, bg="gray", state=tk.DISABLED)
            else:
                btn = tk.Button(frame, width=2, height=1, bg="white", command=lambda x=i, y=j: on_button_click(x, y))
            
            btn.grid(row=i, column=j)
            row.append(btn)
        buttons.append(row)

    fenetre.mainloop()

def modifier_matrice():
    """Met à jour la matrice en fonction des boutons affichés."""
    global matrice
    for x in range(2, 32):  
        for y in range(2, 32): 
            matrice[x][y] = 1 if buttons[x][y]["bg"] == "black" else 0
    return matrice


def bonheur_visuel():
    """Affiche une matrice de bonheur visuel."""
    global matrice
    matrice = module.generer_matrice_magnifique()
    for i in range(2, 32):
        for j in range(2, 32):
            color = "black" if matrice[i][j] == 1 else "white"
            buttons[i][j].config(bg=color)

def effacer():
    """Efface la matrice et remet tous les boutons à blanc."""
    global matrice
    matrice = module.generer_matrice_vide()
    for i in range(2, 32):
        for j in range(2, 32):
            buttons[i][j].config(bg="white")
    return matrice


def on_button_click(x, y):
    """Inverse la couleur d'un bouton lorsqu'il est cliqué."""
    current_color = buttons[x][y]["bg"]
    new_color = "black" if current_color == "white" else "white"
    buttons[x][y].config(bg=new_color)

def aleatoire():
    """Remplit la matrice avec des valeurs aléatoires."""
    global matrice
    matrice = module.generer_matrice_aleatoire()
    for i in range(2, 32):
        for j in range(2, 32):
            color = "black" if matrice[i][j] == 1 else "white"
            buttons[i][j].config(bg=color)




def pause():
    """Met le jeu en pause."""
    global jeu_en_cours
    jeu_en_cours = False  # Stoppe la boucle de génération

def lancer_jeu():
    """Lance l'évolution du jeu de la vie."""
    global matrice, jeu_en_cours
    jeu_en_cours = True

    def boucle_jeu():
        global matrice
        if not jeu_en_cours:
            return  # Si le jeu est en pause, on arrête la boucle
        
        matrice_precedente = modifier_matrice()
        matrice_suivante = module.nouvelle_generation(matrice_precedente)

        # Mise à jour de l'affichage des boutons
        for i in range(2, 32):
            for j in range(2, 32):
                color = "black" if matrice_suivante[i][j] == 1 else "white"
                buttons[i][j].config(bg=color)

        matrice = matrice_suivante  # Mettre à jour la matrice actuelle

        fenetre.after(100, boucle_jeu)  # Répéter la fonction après 100ms

    boucle_jeu()  # Démarrer la boucle du jeu

affichage()
