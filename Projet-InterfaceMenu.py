from tkinter import *
from Puissance4 import *


# Fenetre
MenuInterface = Tk()
MenuInterface.title("Polystation4")
MenuInterface.minsize(1250,700)
MenuInterface.maxsize(1250,750)
MenuInterface.config(bg ="#00BFFF")
MenuInterface.iconbitmap("logo.ico")
# Fonction des boutons 
def Boutton1() :
    print("bouton 1")
def Boutton2() :
    print("bouton 2")
def Boutton3() :
    print("bouton 3")
# Message d'acceuil
Polystation4 = Label(MenuInterface, text="PolyStation4",bg= '#00BFFF', fg = 'Black', font='Calibri, 48')
# Cadre pour les jeux
CadreJeu1 = Frame(MenuInterface,relief="sunken", bd = 2)
CadreJeu2 = Frame(MenuInterface,relief="sunken", bd = 2)
CadreJeu3 = Frame(MenuInterface,relief="sunken", bd = 2 )
# Image des jeux 
ImageJeu1 = PhotoImage(file="ImageJeuVie.png")
ImageJeu2 = PhotoImage(file="ImageJeuDames.png")
ImageJeu3 = PhotoImage(file="ImagePuissance4.png")
# Boutons
BoutonJeu1 = Button(CadreJeu1, image=ImageJeu1, font =("Arial",14), bg = '#00BFFF', command=Boutton1)
BoutonJeu2 = Button(CadreJeu2, image=ImageJeu2, font =("Arial",14), bg = '#00BFFF', command=Boutton2)
BoutonJeu3 = Button(CadreJeu3, image=ImageJeu3, font =("Arial",14),bg = '#00BFFF', command=Boutton3)
# Messages
Polystation4.pack(side="top")
# |-> Cadre jeux
CadreJeu1.place(x = 75, y = 225)
CadreJeu2.place(x = 500, y = 225)
CadreJeu3.place(x = 900, y = 225)
# |-> Boutons de lancement
BoutonJeu1.pack(side="bottom")
BoutonJeu2.pack(side="bottom")
BoutonJeu3.pack(side="bottom")
# |-> fenetre
MenuInterface.mainloop()
