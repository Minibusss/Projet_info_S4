from tkinter import *
#import Jeu_de_la_vie as JV
#import Puissance4
import CodeDames1

def lire_record_dames():
    try:
        with open("Record_Jeux_de_dames.txt", "r", encoding='utf-8') as file:
            lines = file.readlines()
            meilleur_score = float('inf')
            meilleur_joueur = ""
            for i, line in enumerate(lines):
                if "Nombre total de coups :" in line:
                    coups = int(line.split(":")[1].strip())
                    if coups < meilleur_score:
                        meilleur_score = coups
                        if i >= 2 and "Vainqueur :" in lines[i-2]:
                            meilleur_joueur = lines[i-2].split(":")[1].strip()
            if meilleur_score != float('inf'):
                return meilleur_joueur, meilleur_score
    except FileNotFoundError:
        pass
    return None, None

def interface(root, main_frame):
    for w in main_frame.winfo_children():
        w.destroy()

    MenuInterface = Frame(main_frame, bg="#00BFFF")
    MenuInterface.pack(expand=True, fill=BOTH)

    # Titre
    Label(MenuInterface, text="Polystation 4", bg='#00BFFF', fg='black', font=('Calibri', 48)).pack(pady=20)
    

    # Cadres des trois jeux
    '''Cadre1 = Frame(MenuInterface, bd=2, relief="sunken")'''
    Cadre2 = Frame(MenuInterface, bd=2, relief="sunken")
    '''Cadre3 = Frame(MenuInterface, bd=2, relief="sunken")'''
    '''Cadre1.place(x=150,  y=300)'''
    Cadre2.place(x=625,  y=300)
    '''Cadre3.place(x=1100, y=300)'''

    # Chargement des images
    try:
        img1 = PhotoImage(file="ImageJeuVie.png")
        img2 = PhotoImage(file="ImageJeuDames.png")
        img3 = PhotoImage(file="ImagePuissance4.png")
    except:
        img1 = img2 = img3 = None

    # Boutons de lancement
    ''' Bouton1 = Button(Cadre1, image=img1, bg='#00BFFF',
                     command=lambda: JV.affichage(root, main_frame))'''
    Bouton2 = Button(Cadre2, image=img2, bg='#00BFFF',
                     command=lambda: CodeDames1.affichage(root, main_frame))
    '''Bouton3 = Button(Cadre3, image=img3, bg='#00BFFF',
                     command=lambda: Puissance4.affichage(root, main_frame))'''

    '''Bouton1.pack()'''
    Bouton2.pack()
    ''' Bouton3.pack()'''

    # Afficher le record du jeu de dames
    record_joueur, record_coups = lire_record_dames()
    if record_joueur and record_coups:
        Label(Cadre2, 
              text=f"Record : {record_joueur}\n{record_coups} coups", 
              bg='white', 
              fg='black', 
              font=('Calibri', 12)).pack(pady=5)

    # Conserver références aux images
    #MenuInterface.img1 = img1
    MenuInterface.img2 = img2
    #MenuInterface.img3 = img3