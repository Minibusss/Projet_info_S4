from tkinter import *

piece_selectionee = None
coups_possibles = []

def placer_piece(row, col, piece):
    piece.grid(row=row, column=col)
    return piece  # Fonction pour placer une pièce sur le damier


def click_pion(event, row, col):
    global piece_selectionee, coups_possibles
    
    # Reset les couleurs de toutes les cases
    reset_couleurs()
    
    # Enleve le widget "Mouvement invalide"
    for widget in fenetre.grid_slaves(row=8):
        widget.destroy()
    
    # Vérifie si la case est noire (non jouable)
    if (row + col) % 2 != 0:  # Les cases noires sont celles où la somme des coordonnées est paire
        print(f"Case noire non jouable en {row},{col}")
        Label(fenetre, text="Case noire non jouable", bg='red').grid(row=8, column=0, columnspan=8)
        if piece_selectionee is not None:
            piece_selectionee = None
            coups_possibles = []
        return
    
    if piece_selectionee is None:
        # Vérifier si la case contient un pion
        widgets = fenetre.grid_slaves(row=row, column=col)
        if not (widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all()):
            print(f"Pas de pion en {row},{col}")
            Label(fenetre, text="Pas de pion à cette position", bg='red').grid(row=8, column=0, columnspan=8)
            return
            
        # Premier click - selection d'une piece
        piece_selectionee = (row, col)
        print(f"Pion sélectionné en {row},{col}")
        # Met un fond jaune sur la case sélectionnée
        event.widget.configure(bg='yellow')
        coups_possibles, coups_bloques = calcul_coups_possibles(row, col)
        # Met un fond vert sur les cases possibles
        # Met un fond rouge sur les cases bloquées
        montre_coups_possibles(coups_possibles, coups_bloques)
    else:
        # Deuxième click - déplacement de la pièce
        # Vérifier si le mouvement est valide
        if (row, col) in coups_possibles:
            print(f"Déplacement de {piece_selectionee} vers {row},{col}")
            deplacer_piece(piece_selectionee[0], piece_selectionee[1], row, col)
        elif (row, col)==piece_selectionee:
            # Si on clique sur la même case, on annule la sélection
            print(f"Annulation de la sélection de {piece_selectionee}")
            event.widget.configure(bg='white' if (row+col)%2==0 else 'black')
            piece_selectionee = None
       
        else:
            print(f"Mouvement invalide de {piece_selectionee} vers {row},{col}")
            Label(fenetre, text="Mouvement invalide", bg='red').grid(row=8, column=0, columnspan=8)
        # Réinitialiser la sélection de la pièce 
        piece_selectionee = None
        coups_possibles = []
        

def calcul_coups_possibles(row, col):
    moves = []
    coups_bloques = []
    # Déterminer la couleur du pion
    widgets = fenetre.grid_slaves(row=row, column=col)
    if widgets and hasattr(widgets[0], 'find_all'):
        # On vérifie la couleur du pion (oval)
        piece_items = widgets[0].find_all()
        if piece_items:
            piece_color = widgets[0].itemcget(piece_items[0], 'fill')
    else:
        # Si la case est vide, on ne peut pas déterminer la couleur
        piece_color = None
    
    direction = 1 if piece_color == 'white' else -1
    
    # Mouvements simples et captures
    for dx in [-1, 1]:
        new_row = row + direction
        new_col = col + dx
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            # Vérifier si la case est occupée
            widgets = fenetre.grid_slaves(row=new_row, column=new_col)
            if widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all():
                # Case occupée, vérifier si on peut capturer
                piece_items = widgets[0].find_all()
                if piece_items:
                    other_color = widgets[0].itemcget(piece_items[0], 'fill')
                    if other_color != piece_color:  # Pion adverse
                        # Vérifier la case suivante pour la capture
                        capture_row = new_row + direction
                        capture_col = new_col + dx
                        if 0 <= capture_row < 8 and 0 <= capture_col < 8:
                            capture_widgets = fenetre.grid_slaves(row=capture_row, column=capture_col)
                            if not (capture_widgets and hasattr(capture_widgets[0], 'find_all') 
                                  and capture_widgets[0].find_all()):
                                # Case libre après le pion adverse
                                moves.append((capture_row, capture_col))
                coups_bloques.append((new_row, new_col))
            else:
                moves.append((new_row, new_col))

    return moves, coups_bloques

def reset_couleurs():
    for i in range(8):
        for j in range(8):
            widget = fenetre.grid_slaves(row=i, column=j)[0]
            widget.configure(bg='white' if (i+j)%2==0 else 'black')

def montre_coups_possibles(moves, blocked):
    # Afficher les mouvements possibles en vert
    for row, col in moves:
        widget = fenetre.grid_slaves(row=row, column=col)[0]
        widget.configure(bg='lightgreen')
    
    # Afficher les mouvements bloqués en rouge
    for row, col in blocked:
        widget = fenetre.grid_slaves(row=row, column=col)[0]
        widget.configure(bg='red')



def creer_pion(couleur, row, col):
    bg_color = 'white' if (row+col)%2==0 else 'black'
    pion = Canvas(fenetre, width=80, height=80, bg=bg_color)
    pion.create_oval(10, 10, 70, 70, fill=couleur, outline='black' if couleur=='white' else 'white', width=2)
    pion.bind('<Button-1>', lambda event, r=row, c=col: click_pion(event, r, c))
    return pion

def deplacer_piece(old_row, old_col, new_row, new_col):
    # Récupérer la pièce à l'ancienne position
    old_widgets = fenetre.grid_slaves(row=old_row, column=old_col)
    if not old_widgets:
        raise ValueError(f"Pas de pièce à la position : ({old_row}, {old_col})")
    old_piece = old_widgets[0]
    
    # Récupérer la couleur du pion
    piece_items = old_piece.find_all()
    if piece_items:
        piece_color = old_piece.itemcget(piece_items[0], 'fill')
        
        # Supprimer le pion de l'ancienne position
        old_piece.delete("all")
        old_piece.configure(bg='white' if (old_row + old_col) % 2 == 0 else 'black')
        
        # Créer le pion dans la nouvelle position
        new_widgets = fenetre.grid_slaves(row=new_row, column=new_col)
        if new_widgets:
            new_canvas = new_widgets[0]
            new_canvas.configure(bg='white' if (new_row + new_col) % 2 == 0 else 'black')
            new_canvas.create_oval(10, 10, 70, 70, fill=piece_color, 
                                 outline='black' if piece_color=='white' else 'white', width=2)

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Jeu de dames")
fenetre.geometry("1000x750")
fenetre.resizable(width=False, height=False)
fenetre.iconbitmap("dames.ico")

# On créé le damier
for i in range(8):
    for j in range(8):
        frame = Canvas(fenetre, width=80, height=80, bg='white' if (i+j)%2==0 else 'black')
        frame.grid(row=i, column=j)
        frame.bind('<Button-1>', lambda event, r=i, c=j: click_pion(event, r, c))

# Placement des pions
for j in range(3):
    for i in range(0,7,2):
        pion_blanc = creer_pion('white', j, i if j%2==0 else i+1)
        placer_piece(j, i if j%2==0 else i+1, pion_blanc)
    for k in range(1,8,2):
        pion_noir = creer_pion('black', 7-j, k if j%2==0 else k-1)
        placer_piece(7-j, k if j%2==0 else k-1, pion_noir)

fenetre.mainloop()