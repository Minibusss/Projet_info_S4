import tkinter as tk
import Jeu_de_la_vie_Main as module

def affichage():
    global buttons
    fenetre = tk.Tk()
    fenetre.title("Jeu de la vie")
    fenetre.geometry("800x800") 
    fenetre.iconbitmap("logo.ico")
    fenetre.config(background='#FFFFFF')

    frame = tk.Frame(fenetre, bg='#FFFFFF', bd=1, relief=tk.SUNKEN)
    frame.pack(expand=tk.YES)

    

    buttons = []

    for i in range(30):
        row = []
        for j in range(30):
            btn = tk.Button(frame, width=2, height=1, bg="white", command=lambda x=i, y=j: on_button_click(x, y))
            btn.grid(row=i, column=j)
            row.append(btn)
        buttons.append(row)


    fenetre.mainloop()

matrice = module.generer_matrice_vide()

# tu dois ajuster ajuster le x et y pour que l'affichage sois pas sur les bord de la matrice......
def modifier_matrice(matrice, x, y):
    #for ......
        #for ......
            if buttons[x][y]["bg"] == "black":
                matrice[x][y] = 1
            else:
                matrice[x][y] = 0

def on_button_click(x, y):
        current_color = buttons[x][y]["bg"]
        new_color = "black" if current_color == "white" else "white"
        buttons[x][y].config(bg=new_color)


