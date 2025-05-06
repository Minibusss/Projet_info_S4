from tkinter import *
from tkinter import messagebox
import datetime

# Variables globales
piece_selectionee = None
coups_possibles = []
CASES_JOUABLES = 'white'
tour_blanc = True
cadre_jeu = None
player1 = None
player2 = None
entry_joueur1 = None
entry_joueur2 = None
label_joueur1 = None
label_joueur2 = None

nombre_coups = 0
joueur1 = ""
joueur2 = ""

captures_blancs = 0
captures_noirs = 0
deplacements_blancs = 0
deplacements_noirs = 0

def affichage(root, main_frame):
    global cadre_jeu, piece_selectionee, coups_possibles, tour_blanc, nombre_coups, joueur1, joueur2
 
    # Réinitialisation de l'état du jeu
    piece_selectionee = None
    coups_possibles = []
    tour_blanc = True
    nombre_coups = 0  # Reset move counter
 
    # Efface l'ancien écran
    for widget in main_frame.winfo_children():
        widget.destroy()
 
    # Titre
    titre = Label(main_frame, text="JEU DE DAMES", font=('Arial', 24, 'bold'), pady=20)
    titre.pack()
 
    # Conteneur horizontal centré
    conteneur = Frame(main_frame)
    conteneur.place(relx=0.5, rely=0.5, anchor='center')
 
    # Cadre du damier
    cadre_jeu = Frame(conteneur)
    cadre_jeu.pack(side=LEFT, padx=20, pady=20)
 
    # Cadre des boutons
    cadre_boutons = Frame(conteneur)
    cadre_boutons.pack(side=LEFT, padx=20, pady=20)
 
    label_joueur1 = Label(cadre_boutons, text="Nom Joueur 1 :", font=('Arial', 12))
    entry_joueur1 = Entry(cadre_boutons, font=('Arial', 12))
    label_joueur2 = Label(cadre_boutons, text="Nom Joueur 2 :", font=('Arial', 12))
    entry_joueur2 = Entry(cadre_boutons, font=('Arial', 12))
 
    label_joueur1.pack(pady=(0,5))
    entry_joueur1.pack(pady=(0,10))
    label_joueur2.pack(pady=(0,5))
    entry_joueur2.pack(pady=(0,10))
   
    def valider_nom():
        global joueur1, joueur2
 
        j1 = entry_joueur1.get().strip()
        j2 = entry_joueur2.get().strip()
 
        if j1 and j2:
            joueur1 = j1
            joueur2 = j2
 
            # Détruire les champs et labels
            entry_joueur1.destroy()
            entry_joueur2.destroy()
            label_joueur1.destroy()
            label_joueur2.destroy()
 
            messagebox.showinfo("Noms enregistrés", f"Joueur 1 : {joueur1}\nJoueur 2 : {joueur2}")
        else:
            messagebox.showwarning("Champs vides", "Veuillez saisir un nom pour chaque joueur.")
   
    # Bouton valider nom des joueurs
    bouton_valider = Button(
        cadre_boutons, text="valider", font=('Arial', 12),
        command=valider_nom, pady=10, padx=20, bg='white'
    )
    bouton_valider.pack(pady=(0,20))
   
    # Bouton retour
    bouton_retour = Button(
        cadre_boutons, text="Retour au menu", font=('Arial', 12),
        command=lambda: __import__('InterfaceMenu').interface(root, main_frame),
        pady=10, padx=20, bg='white'
    )
    bouton_retour.pack(pady=(0,20))
 
    # Crée le damier et place les pions
    creer_damier()
    placer_pions_initiaux()
 
    # Indicateur du tour
    Label(cadre_jeu, text="Tour des blancs", bg='white').grid(row=8, column=0, columnspan=8)
 
def est_case_jouable(row, col):
    return (row + col) % 2 == (1 if CASES_JOUABLES == 'white' else 0)
 
def placer_piece(row, col, piece):
    piece.grid(row=row, column=col)
    return piece
 
def creer_damier():
    for i in range(8):
        for j in range(8):
            bg_color = 'white' if (i + j) % 2 == 0 else 'black'
            case = Canvas(cadre_jeu, width=80, height=80, bg=bg_color)
            case.grid(row=i, column=j)
            case.bind('<Button-1>', lambda e, r=i, c=j: click_pion(e, r, c))
 
def creer_pion(couleur, row, col):
    bg_color = 'white' if (row + col) % 2 == 0 else 'black'
    pion = Canvas(cadre_jeu, width=80, height=80, bg=bg_color)
    pion.create_oval(10, 10, 70, 70, fill=couleur,
                     outline='black' if couleur == 'white' else 'white', width=2)
    pion.bind('<Button-1>', lambda e, r=row, c=col: click_pion(e, r, c))
    return pion
 
def placer_pions_initiaux():
    for j in range(3):
        for i in range(0, 7, 2):
            col = i if (j % 2 == (0 if CASES_JOUABLES == 'black' else 1)) else i + 1
            p = creer_pion('white', j, col)
            placer_piece(j, col, p)
        for k in range(1, 8, 2):
            col = k if (j % 2 == (0 if CASES_JOUABLES == 'black' else 1)) else k - 1
            p = creer_pion('black', 7 - j, col)
            placer_piece(7 - j, col, p)
 
def click_pion(event, row, col):
    global piece_selectionee, coups_possibles, tour_blanc, nombre_coups
 
    # Réinitialise l'affichage
    reset_couleurs()
    for w in cadre_jeu.grid_slaves(row=8):
        w.destroy()
 
    # Case non jouable ?
    if not est_case_jouable(row, col):
        Label(cadre_jeu, text="Case non jouable", bg='red').grid(row=8, column=0, columnspan=8)
        piece_selectionee = None
        coups_possibles = []
        return
 
    widgets = cadre_jeu.grid_slaves(row=row, column=col)
    # Si aucune pièce sélectionnée -> sélectionner
    if piece_selectionee is None:
        if not (widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all()):
            Label(cadre_jeu, text="Pas de pion", bg='red').grid(row=8, column=0, columnspan=8)
            return
        color = widgets[0].itemcget(widgets[0].find_all()[0], 'fill')
        if (color == 'white' and not tour_blanc) or (color == 'black' and tour_blanc):
            Label(cadre_jeu, text=f"Tour des {'blancs' if tour_blanc else 'noirs'}", bg='red')\
                .grid(row=8, column=0, columnspan=8)
            return
        piece_selectionee = (row, col)
        event.widget.configure(bg='yellow')
        coups_possibles, blocs = calcul_coups_possibles(row, col)
        montre_coups_possibles(coups_possibles, blocs)
 
    # Sinon -> déplacement ou annulation
    else:
        if (row, col) in coups_possibles:
            # Increment move counter when a piece is moved
            nombre_coups += 1
            
            cont = deplacer_piece(piece_selectionee[0], piece_selectionee[1], row, col)
            # si capture multiple
            if cont:
                piece_selectionee = (row, col)
                coups_possibles, blocs = calcul_coups_possibles(row, col)
                if coups_possibles:
                    montre_coups_possibles(coups_possibles, blocs)
                    return
            # fin de tour
            piece_selectionee = None
            coups_possibles = []
            tour_blanc = not tour_blanc
            vic = verifier_victoire()
            if vic:
                gagnant = joueur1 if (vic == 'blancs') else joueur2
                perdant = joueur2 if (vic == 'blancs') else joueur1
                
                message = f"{gagnant} a gagné !\n{perdant} a perdu !\n\nNombre de coups : {nombre_coups}"
                Label(cadre_jeu, text=message, bg='gold', font=('Arial',14,'bold'))\
                    .grid(row=8, column=0, columnspan=8)
                
                # Save detailed game stats
                today = datetime.datetime.today()
                with open("Record_Jeux_de_dames.txt", "a", encoding='utf-8') as Stats:
                    Stats.write(f'''
=== Partie du {today.strftime("%Y-%m-%d %H:%M:%S")} ===
Vainqueur : {gagnant} ({vic})
Perdant : {perdant}
Nombre total de coups : {nombre_coups}

Statistiques blancs ({joueur1}) :
- Déplacements : {deplacements_blancs}
- Captures : {captures_blancs}

Statistiques noirs ({joueur2}) :
- Déplacements : {deplacements_noirs}
- Captures : {captures_noirs}

--------------------------------
''')
                
                # désactive tous les clics
                for i in range(8):
                    for j in range(8):
                        w = cadre_jeu.grid_slaves(row=i, column=j)[0]
                        w.unbind('<Button-1>')
            else:
                Label(cadre_jeu, text=f"Tour des {'blancs' if tour_blanc else 'noirs'}", bg='white')\
                    .grid(row=8, column=0, columnspan=8)
 
        elif (row, col) == piece_selectionee:
            # annule la sélection
            event.widget.configure(bg='white' if (row+col)%2==0 else 'black')
            piece_selectionee = None
        else:
            Label(cadre_jeu, text="Mouvement invalide", bg='red')\
                .grid(row=8, column=0, columnspan=8)
            piece_selectionee = None
            coups_possibles = []
 
def calcul_coups_possibles(row, col):
    moves, blocs, captures = [], [], []
    widgets = cadre_jeu.grid_slaves(row=row, column=col)
    if widgets and hasattr(widgets[0], 'find_all'):
        couleur = widgets[0].itemcget(widgets[0].find_all()[0], 'fill')
        is_dame = len(widgets[0].find_all()) > 1
        captures = cherche_captures(row, col, couleur, [])
        if captures:
            return captures, blocs
        if is_dame:
            for dy in (-1,1):
                for dx in (-1,1):
                    cr, cc = row, col
                    while True:
                        nr, nc = cr+dy, cc+dx
                        if not (0<=nr<8 and 0<=nc<8): break
                        w2 = cadre_jeu.grid_slaves(row=nr, column=nc)
                        if w2 and hasattr(w2[0], 'find_all') and w2[0].find_all():
                            blocs.append((nr,nc)); break
                        else:
                            moves.append((nr,nc))
                        cr, cc = nr, nc
        else:
            direction = 1 if couleur=='white' else -1
            for dx in (-1,1):
                nr, nc = row+direction, col+dx
                if 0<=nr<8 and 0<=nc<8:
                    w2 = cadre_jeu.grid_slaves(row=nr, column=nc)
                    if w2 and hasattr(w2[0], 'find_all') and w2[0].find_all():
                        blocs.append((nr,nc))
                    else:
                        moves.append((nr,nc))
    return moves, blocs
 
def cherche_captures(row, col, couleur, visited=None):
    if visited is None:
        visited = []
    captures = []
    widgets = cadre_jeu.grid_slaves(row=row, column=col)
    # on récupère le canvas de la case
    if not widgets:
        return captures
    case_canvas = widgets[0]
    is_dame = len(case_canvas.find_all()) > 1
 
    if is_dame:
        for dy in (-1, 1):
            for dx in (-1, 1):
                cr, cc = row, col
                piece_trouvee = None
                while True:
                    nr, nc = cr + dy, cc + dx
                    if not (0 <= nr < 8 and 0 <= nc < 8):
                        break
                    w2 = cadre_jeu.grid_slaves(row=nr, column=nc)
                    if w2 and w2[0].find_all():
                        # pièce rencontrée
                        if piece_trouvee:
                            break
                        other_color = w2[0].itemcget(w2[0].find_all()[0], 'fill')
                        if other_color != couleur:
                            piece_trouvee = (nr, nc)
                        else:
                            break
                    elif piece_trouvee:
                        # case vide après pièce adverse → capture possible
                        if (nr, nc) not in visited:
                            captures.append((nr, nc))
                            # captures en chaîne
                            captures += cherche_captures(nr, nc, couleur, visited + [(row, col)])
                    cr, cc = nr, nc
    else:
        # pion normal : on cherche en deux pas
        for dy in (-1, 1):
            for dx in (-1, 1):
                nr, nc = row + 2 * dy, col + 2 * dx
                mid_r, mid_c = row + dy, col + dx
                if 0 <= nr < 8 and 0 <= nc < 8:
                    mid_widgets = cadre_jeu.grid_slaves(row=mid_r, column=mid_c)
                    if (mid_widgets and mid_widgets[0].find_all()):
                        other_color = mid_widgets[0].itemcget(mid_widgets[0].find_all()[0], 'fill')
                        dest_widgets = cadre_jeu.grid_slaves(row=nr, column=nc)
                        if other_color != couleur and (not dest_widgets or not dest_widgets[0].find_all()):
                            if (nr, nc) not in visited:
                                captures.append((nr, nc))
                                captures += cherche_captures(nr, nc, couleur, visited + [(row, col)])
    return captures
 
def reset_couleurs():
    for i in range(8):
        for j in range(8):
            w = cadre_jeu.grid_slaves(row=i, column=j)[0]
            w.configure(bg='white' if (i+j)%2==0 else 'black')
 
def montre_coups_possibles(moves, blocked):
    for r,c in moves:
        cadre_jeu.grid_slaves(row=r, column=c)[0].configure(bg='lightgreen')
    for r,c in blocked:
        cadre_jeu.grid_slaves(row=r, column=c)[0].configure(bg='red')
 
def deplacer_piece(orow, ocol, nrow, ncol):
    global captures_blancs, captures_noirs, deplacements_blancs, deplacements_noirs
    
    old = cadre_jeu.grid_slaves(row=orow, column=ocol)[0]
    items = old.find_all()
    if not items: return False
    couleur = old.itemcget(items[0],'fill')
    is_dame = len(items)>1
    
    # Compter les déplacements
    if couleur == 'white':
        deplacements_blancs += 1
    else:
        deplacements_noirs += 1
    
    # gestion capture
    if abs(nrow-orow)>1:
        if is_dame:
            dy = 1 if nrow>orow else -1
            dx = 1 if ncol>ocol else -1
            cr, cc = orow, ocol
            while (cr,cc)!=(nrow,ncol):
                cr+=dy; cc+=dx
                w2 = cadre_jeu.grid_slaves(row=cr, column=cc)[0]
                if w2.find_all():
                    w2.delete("all")
                    w2.configure(bg='white' if (cr+cc)%2==0 else 'black')
                    # Compter les captures
                    if couleur == 'white':
                        captures_blancs += 1
                    else:
                        captures_noirs += 1
                    break
        else:
            cr, cc = (orow+nrow)//2, (ocol+ncol)//2
            w2 = cadre_jeu.grid_slaves(row=cr, column=cc)[0]
            w2.delete("all")
            w2.configure(bg='white' if (cr+cc)%2==0 else 'black')
            # Compter les captures
            if couleur == 'white':
                captures_blancs += 1
            else:
                captures_noirs += 1

    # Nouvelle version : on conserve is_already_dame et on ajoute la couronne si c'était déjà une dame
    old.delete("all")
    old.configure(bg='white' if (orow+ocol)%2==0 else 'black')
 
    new = cadre_jeu.grid_slaves(row=nrow, column=ncol)[0]
    new.configure(bg='white' if (nrow+ncol)%2==0 else 'black')
 
    # On dessine toujours le pion
    new.create_oval(10,10,70,70,
                    fill=couleur,
                    outline='black' if couleur=='white' else 'white',
                    width=2)
 
    # On dessine la couronne si :
    #  • c'était déjà une dame
    #  • ou si on vient tout juste d'être promu
    if is_dame or (not is_dame and ((couleur=='white' and nrow==7) or (couleur=='black' and nrow==0))):
        new.create_oval(20,20,60,60,
                        fill='gold',
                        outline='black' if couleur=='white' else 'white',
                        width=2)
    is_dame = True
    cadre_jeu.update()
    return abs(nrow-orow)>1 and bool(cherche_captures(nrow, ncol, couleur, []))
 
def verifier_victoire():
    wb = bn = False
    for i in range(8):
        for j in range(8):
            w = cadre_jeu.grid_slaves(row=i,column=j)[0]
            items = w.find_all()
            if items:
                color = w.itemcget(items[0],'fill')
                coups,_ = calcul_coups_possibles(i,j)
                if color=='white': wb |= bool(coups)
                else: bn |= bool(coups)
    if not wb: return 'noirs'
    if not bn: return 'blancs'
    return None