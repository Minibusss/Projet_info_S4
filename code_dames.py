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
    
    # Remove any existing "Mouvement invalide" label
    for widget in fenetre.grid_slaves(row=8):
        widget.destroy()
    
    if piece_selectionee is None:
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
        # On vérifie la couleur du pion (oval) et non pas le fond
        piece_items = widgets[0].find_all()
        if piece_items:
            piece_color = widgets[0].itemcget(piece_items[0], 'fill')
    else:
    # Si la case est vide, on ne peut pas déterminer la couleur
        piece_color = None
    
    direction = 1 if piece_color == 'white' else -1
    
    # Mouvements simples
    for dx in [-1, 1]:
        new_row = row + direction
        new_col = col + dx
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            # Vérifier si la case est occupée
            widgets = fenetre.grid_slaves(row=new_row, column=new_col)
            if widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all():
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
    
    # Supprimer l'ancienne pièce
    old_piece.destroy()
    
    # Créer une nouvelle case vide à l'ancienne position
    old_bg = 'white' if (old_row + old_col) % 2 == 0 else 'black'
    frame = Frame(fenetre, width=80, height=80, bg=old_bg)
    frame.grid(row=old_row, column=old_col)
    
    # Créer et placer la nouvelle pièce
    new_piece = creer_pion(piece_color, new_row, new_col)
    placer_piece(new_row, new_col, new_piece)

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Jeu de dames")
fenetre.geometry("1000x750")
fenetre.resizable(width=False, height=False)
fenetre.iconbitmap("dames.ico")

# On créé le damier
for i in range(8):
    for j in range(8):
        frame = Frame(fenetre, width=80, height=80, bg='white' if (i+j)%2==0 else 'black')
        frame.grid(row=i, column=j)

# Placement des pions
for j in range(3):
    for i in range(0,7,2):
        pion_blanc = creer_pion('white', j, i if j%2==0 else i+1)
        placer_piece(j, i if j%2==0 else i+1, pion_blanc)
    for k in range(1,8,2):
        pion_noir = creer_pion('black', 7-j, k if j%2==0 else k-1)
        placer_piece(7-j, k if j%2==0 else k-1, pion_noir)

fenetre.mainloop()