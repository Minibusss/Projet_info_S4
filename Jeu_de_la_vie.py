import tkinter as tk
import Jeu_de_la_vie_Main as module

def affichage():
    global buttons
    fenetre = tk.Tk()
    fenetre.title("Jeu de la vie")
    fenetre.geometry("1000x9000") 
    fenetre.iconbitmap("logo.ico")
    fenetre.config(background='#FFFFFF')

    # Création d'un Frame pour aligner les boutons horizontalement en bas
    frame_boutons = tk.Frame(fenetre, bg="white")
    frame_boutons.pack(side=tk.TOP, pady=10)  # Place le frame en bas de la fenêtre

    frame = tk.Frame(fenetre, bg='#FFFFFF', bd=1, relief=tk.SUNKEN)
    frame.pack(expand=tk.YES)

    
    matrice = module.generer_matrice_vide()
    print(matrice)

    # tu dois trouver le moyen de passer la matrice, X et Y en paramètre de la fonction grâce à lambda
    # il faut donc trouve un moyen dans le meme style que  current_color = buttons[x][y]["bg"] mais pour récuperer x et Y ou alors juste le numero de la case ( et ensuite diviser par le nm de rangée pour avoir x et y)
    monBouton1 = tk.Button(frame_boutons, text="Lancer le jeu", bg="white", command=lambda x=matrice, y=j+2, matrice = matrice : modifier_matrice(matrice, x, y))
    monBouton2 = tk.Button(frame_boutons, text="Pause", bg="white",command=lambda x=i+2, y=j+2, matrice = matrice : modifier_matrice(matrice, x, y))            

    buttons = []

    for i in range(1,31):
        row = []
        for j in range(1,31):
            btn = tk.Button(frame, width=2, height=1, bg="white", command=lambda x=i, y=j: on_button_click(x, y))
            btn.grid(row=i, column=j)
            row.append(btn)
        buttons.append(row)

    monBouton1.pack(side=tk.LEFT, padx=5)
    monBouton2.pack(side=tk.LEFT, padx=5)  
    fenetre.mainloop()




def modifier_matrice(matrice, x, y):
    for _ in range(30):
        for _ in range(30):
            if buttons[x][y]["bg"] == "black":
                matrice[x][y] = 1
            else:
                matrice[x][y] = 0
    print(matrice)

def on_button_click(x, y):
        current_color = buttons[x][y]["bg"]
        new_color = "black" if current_color == "white" else "white"
        buttons[x][y].config(bg=new_color)

affichage()


