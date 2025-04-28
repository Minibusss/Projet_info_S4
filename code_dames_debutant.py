from tkinter import *

piece_selectionee = None
coups_possibles = []
CASES_JOUABLES = 'white'  # ou 'white' pour jouer sur les cases noires
tour_blanc = True  # True pour les blancs, False pour les noirs

def est_case_jouable(row, col):
    #Vérifie si une case est jouable selon la configuration
    return (row + col) % 2 == (1 if CASES_JOUABLES == 'white' else 0)

def placer_piece(row, col, piece):
    piece.grid(row=row, column=col)
    return piece  # Fonction pour placer une pièce sur le damier

def click_pion(event, row, col):
    global piece_selectionee, coups_possibles, tour_blanc
    
    # Reset les couleurs de toutes les cases
    reset_couleurs()
    
    # Enleve le widget "Mouvement invalide"
    for widget in cadre_jeu.grid_slaves(row=8):
        widget.destroy()
    
    # Vérifie si la case est jouable
    if not est_case_jouable(row, col):
        print(f"Case {CASES_JOUABLES=='black' and 'noire' or 'blanche'} non jouable en {row},{col}")
        Label(cadre_jeu, text=f"Case {CASES_JOUABLES=='black' and 'noire' or 'blanche'} non jouable", 
              bg='red').grid(row=8, column=0, columnspan=8)
        if piece_selectionee is not None:
            piece_selectionee = None
            coups_possibles = []
        return
    
    if piece_selectionee is None:
        # Vérifier si la case contient un pion
        widgets = cadre_jeu.grid_slaves(row=row, column=col)
        if not (widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all()):
            print(f"Pas de pion en {row},{col}")
            Label(cadre_jeu, text="Pas de pion à cette position", bg='red').grid(row=8, column=0, columnspan=8)
            return
        
        # Vérifier si c'est le bon tour
        piece_items = widgets[0].find_all()
        piece_color = widgets[0].itemcget(piece_items[0], 'fill')
        if (piece_color == 'white' and not tour_blanc) or (piece_color == 'black' and tour_blanc):
            print(f"Ce n'est pas votre tour")
            Label(cadre_jeu, text=f"Tour des {tour_blanc and 'blancs' or 'noirs'}", 
                  bg='red').grid(row=8, column=0, columnspan=8)
            return
            
        # Premier click - selection d'une piece
        piece_selectionee = (row, col)
        print(f"Pion sélectionné en {row},{col}")
        event.widget.configure(bg='yellow')
        coups_possibles, coups_bloques = calcul_coups_possibles(row, col)
        montre_coups_possibles(coups_possibles, coups_bloques)
    else:
        # Deuxième click - déplacement de la pièce
        if (row, col) in coups_possibles:
            print(f"Déplacement de {piece_selectionee} vers {row},{col}")
            autres_captures = deplacer_piece(piece_selectionee[0], piece_selectionee[1], row, col)
            
            if autres_captures:
                # Continuer avec le même pion
                piece_selectionee = (row, col)
                coups_possibles, coups_bloques = calcul_coups_possibles(row, col)
                if coups_possibles:  # S'il y a des captures possibles
                    montre_coups_possibles(coups_possibles, coups_bloques)
                    return  # Continue le tour
            
            # Sinon, fin du tour
            piece_selectionee = None
            coups_possibles = []
            tour_blanc = not tour_blanc
            
            # Vérifier s'il y a un gagnant
            gagnant = verifier_victoire()
            if gagnant:
                message = f"Victoire des {gagnant} !"
                Label(cadre_jeu, text=message, bg='gold', font=('Arial', 14, 'bold')).grid(
                    row=8, column=0, columnspan=8)
                # Désactiver les événements de click
                for i in range(8):
                    for j in range(8):
                        widgets = cadre_jeu.grid_slaves(row=i, column=j)
                        if widgets:
                            widgets[0].unbind('<Button-1>')
            else:
                Label(cadre_jeu, text=f"Tour des {tour_blanc and 'blancs' or 'noirs'}", 
                      bg='white').grid(row=8, column=0, columnspan=8)
        elif (row, col)==piece_selectionee:
            print(f"Annulation de la sélection de {piece_selectionee}")
            event.widget.configure(bg='white' if (row+col)%2==0 else 'black')
            piece_selectionee = None
        else:
            print(f"Mouvement invalide de {piece_selectionee} vers {row},{col}")
            Label(cadre_jeu, text="Mouvement invalide", bg='red').grid(row=8, column=0, columnspan=8)
        
        piece_selectionee = None
        coups_possibles = []

def calcul_coups_possibles(row, col):
    moves = []
    coups_bloques = []
    captures = []
    
    widgets = cadre_jeu.grid_slaves(row=row, column=col)
    if widgets and hasattr(widgets[0], 'find_all'):
        piece_items = widgets[0].find_all()
        if piece_items:
            piece_color = widgets[0].itemcget(piece_items[0], 'fill')
            is_dame = len(widgets[0].find_all()) > 1  # Vérifie si c'est une dame
            
            # Vérifie les captures dans toutes les directions
            captures = cherche_captures(row, col, piece_color, [])
            
            # Si des captures sont possibles, ce sont les seuls coups permis
            if captures:
                return captures, coups_bloques
            
            # Pour une dame, on peut bouger dans toutes les directions sur plusieurs cases
            if is_dame:
                for direction_y in [-1, 1]:  # Haut et bas
                    for direction_x in [-1, 1]:  # Gauche et droite
                        current_row = row
                        current_col = col
                        while True:
                            new_row = current_row + direction_y
                            new_col = current_col + direction_x
                            
                            # Vérifier si on est toujours sur le damier
                            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                                break
                                
                            # Vérifier si la case est occupée
                            widgets = cadre_jeu.grid_slaves(row=new_row, column=new_col)
                            if widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all():
                                coups_bloques.append((new_row, new_col))
                                break
                            else:
                                moves.append((new_row, new_col))
                            
                            current_row = new_row
                            current_col = new_col
            else:
                # Pour un pion normal, la direction dépend de la couleur
                direction = 1 if piece_color == 'white' else -1
                for dx in [-1, 1]:  # Gauche et droite
                    new_row = row + direction
                    new_col = col + dx
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        widgets = cadre_jeu.grid_slaves(row=new_row, column=new_col)
                        if widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all():
                            coups_bloques.append((new_row, new_col))
                        else:
                            moves.append((new_row, new_col))
    
    return moves, coups_bloques

def cherche_captures(row, col, piece_color, chemin_parcouru=None):
    if chemin_parcouru is None:
        chemin_parcouru = []
    
    captures = []
    widgets = cadre_jeu.grid_slaves(row=row, column=col)
    is_dame = len(widgets[0].find_all()) > 1 if widgets else False
    
    # Pour une dame, on cherche dans toutes les directions diagonales jusqu'à trouver une pièce
    if is_dame:
        for direction_y in [-1, 1]:  # Haut et bas
            for direction_x in [-1, 1]:  # Gauche et droite
                current_row = row
                current_col = col
                piece_trouvee = None
                
                while True:
                    new_row = current_row + direction_y
                    new_col = current_col + direction_x
                    
                    # Sortie du damier
                    if not (0 <= new_row < 8 and 0 <= new_col < 8):
                        break
                    
                    # Vérifie si la case contient une pièce
                    widgets = cadre_jeu.grid_slaves(row=new_row, column=new_col)
                    if widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all():
                        if piece_trouvee:  # Deuxième pièce trouvée = impossible de capturer
                            break
                        piece_items = widgets[0].find_all()
                        other_color = widgets[0].itemcget(piece_items[0], 'fill')
                        if other_color != piece_color:  # Pièce adverse trouvée
                            piece_trouvee = (new_row, new_col)
                        else:  # Pièce de même couleur = bloqué
                            break
                    elif piece_trouvee:  # Case vide après une pièce adverse = capture possible
                        if (new_row, new_col) not in chemin_parcouru:
                            captures.append((new_row, new_col))
                            # Cherche d'autres captures possibles après celle-ci
                            suites = cherche_captures(new_row, new_col, piece_color, 
                                                    chemin_parcouru + [(row, col)])
                            captures.extend(suites)
                    
                    current_row = new_row
                    current_col = new_col
    else:
        # Pour un pion normal, on peut capturer dans toutes les directions
        for direction in [-1, 1]:  # On autorise les deux directions (avant et arrière)
            for dx in [-1, 1]:  # Gauche et droite
                new_row = row + direction * 2
                new_col = col + dx * 2
                
                # Position du pion à capturer
                capture_row = row + direction
                capture_col = col + dx
                
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    # Vérifie le pion à capturer
                    capture_widgets = cadre_jeu.grid_slaves(row=capture_row, column=capture_col)
                    if (capture_widgets and hasattr(capture_widgets[0], 'find_all') 
                        and capture_widgets[0].find_all()):
                        capture_items = capture_widgets[0].find_all()
                        other_color = capture_widgets[0].itemcget(capture_items[0], 'fill')
                        
                        # Vérifie la case d'arrivée
                        dest_widgets = cadre_jeu.grid_slaves(row=new_row, column=new_col)
                        if (other_color != piece_color and dest_widgets 
                            and not (hasattr(dest_widgets[0], 'find_all') 
                            and dest_widgets[0].find_all())):
                            if (new_row, new_col) not in chemin_parcouru:
                                captures.append((new_row, new_col))
                                suites = cherche_captures(new_row, new_col, piece_color, 
                                                        chemin_parcouru + [(row, col)])
                                captures.extend(suites)
    
    return captures

def reset_couleurs():
    for i in range(8):
        for j in range(8):
            widget = cadre_jeu.grid_slaves(row=i, column=j)[0]
            widget.configure(bg='white' if (i+j)%2==0 else 'black')

def montre_coups_possibles(moves, blocked):
    # Afficher les mouvements possibles en vert
    for row, col in moves:
        widget = cadre_jeu.grid_slaves(row=row, column=col)[0]
        widget.configure(bg='lightgreen')
    
    # Afficher les mouvements bloqués en rouge
    for row, col in blocked:
        widget = cadre_jeu.grid_slaves(row=row, column=col)[0]
        widget.configure(bg='red')

def creer_pion(couleur, row, col):
    bg_color = 'white' if (row+col)%2==0 else 'black'
    pion = Canvas(cadre_jeu, width=80, height=80, bg=bg_color)
    pion.create_oval(10, 10, 70, 70, fill=couleur, outline='black' if couleur=='white' else 'white', width=2)
    pion.bind('<Button-1>', lambda event, r=row, c=col: click_pion(event, r, c))
    return pion

def deplacer_piece(old_row, old_col, new_row, new_col):
    # Récupérer la pièce à l'ancienne position
    old_widgets = cadre_jeu.grid_slaves(row=old_row, column=old_col)
    if not old_widgets:
        raise ValueError(f"Pas de pièce à la position : ({old_row}, {old_col})")
    old_piece = old_widgets[0]
    
    # Récupérer la couleur du pion et vérifier si c'est une dame
    piece_items = old_piece.find_all()
    if not piece_items:
        return
    piece_color = old_piece.itemcget(piece_items[0], 'fill')
    is_already_dame = len(piece_items) > 1  # Vérifie si c'était déjà une dame
    
    # Vérifier s'il y a capture (distance > 1)
    if abs(new_row - old_row) > 1:
        # Pour une dame, on doit trouver le pion capturé sur la diagonale
        if is_already_dame:
            direction_y = 1 if new_row > old_row else -1
            direction_x = 1 if new_col > old_col else -1
            current_row = old_row
            current_col = old_col
            
            # Parcourir la diagonale jusqu'à trouver le pion à capturer
            while current_row != new_row and current_col != new_col:
                current_row += direction_y
                current_col += direction_x
                widgets = cadre_jeu.grid_slaves(row=current_row, column=current_col)
                if widgets and hasattr(widgets[0], 'find_all') and widgets[0].find_all():
                    # Pion trouvé, on le supprime
                    widgets[0].delete("all")
                    widgets[0].configure(bg='white' if (current_row + current_col) % 2 == 0 else 'black')
                    break
        else:
            # Pour un pion normal, on utilise le milieu
            captured_row = (old_row + new_row) // 2
            captured_col = (old_col + new_col) // 2
            captured_widgets = cadre_jeu.grid_slaves(row=captured_row, column=captured_col)
            if captured_widgets:
                captured_piece = captured_widgets[0]
                captured_piece.delete("all")
                captured_piece.configure(bg='white' if (captured_row + captured_col) % 2 == 0 else 'black')
    
    # Supprimer le pion de l'ancienne position
    old_piece.delete("all")
    old_piece.configure(bg='white' if (old_row + old_col) % 2 == 0 else 'black')
    
    # Créer le pion dans la nouvelle position
    new_widgets = cadre_jeu.grid_slaves(row=new_row, column=new_col)
    if new_widgets:
        new_canvas = new_widgets[0]
        new_canvas.configure(bg='white' if (new_row + new_col) % 2 == 0 else 'black')
        
        # Devient ou reste une dame si :
        # - c'était déjà une dame
        # - ou si on atteint la dernière rangée
        is_dame = is_already_dame or (piece_color == 'white' and new_row == 7) or (piece_color == 'black' and new_row == 0)
        
        # Dessiner le pion
        new_canvas.create_oval(10, 10, 70, 70, fill=piece_color, 
                             outline='black' if piece_color=='white' else 'white', width=2)
        # Si c'est une dame, ajouter la couronne
        if is_dame:
            new_canvas.create_oval(20, 20, 60, 60, fill='gold', 
                                 outline='black' if piece_color=='white' else 'white', width=2)
    
    # Vérifier s'il y a d'autres captures possibles
    if abs(new_row - old_row) > 1:
        captures = cherche_captures(new_row, new_col, piece_color)
        if captures:
            # Ne pas changer de tour si d'autres captures sont possibles
            return True
    return False

def creer_damier():
    """Crée le damier avec la bonne configuration des cases jouables"""
    for i in range(8):
        for j in range(8):
            # Inverse les couleurs si on joue sur les cases blanches
            bg_color = 'white' if (i+j)%2==0 else 'black'
            frame = Canvas(cadre_jeu, width=80, height=80, bg=bg_color)
            frame.grid(row=i, column=j)
            frame.bind('<Button-1>', lambda event, r=i, c=j: click_pion(event, r, c))

def placer_pions_initiaux():
    """Place les pions selon la configuration des cases jouables"""
    for j in range(3):
        for i in range(0,7,2):
            # Ajuste la position selon les cases jouables
            col = i if (j%2 == (0 if CASES_JOUABLES == 'black' else 1)) else i+1
            pion_blanc = creer_pion('white', j, col)
            placer_piece(j, col, pion_blanc)
        for k in range(1,8,2):
            # Ajuste la position selon les cases jouables
            col = k if (j%2 == (0 if CASES_JOUABLES == 'black' else 1)) else k-1
            pion_noir = creer_pion('black', 7-j, col)
            placer_piece(7-j, col, pion_noir)

def verifier_victoire():
    """Vérifie s'il y a un gagnant"""
    pieces_blanches = 0
    pieces_noires = 0
    mouvements_blancs = False
    mouvements_noirs = False
    
    # Compte les pièces et vérifie les mouvements possibles
    for i in range(8):
        for j in range(8):
            widgets = cadre_jeu.grid_slaves(row=i, column=j)
            if widgets and hasattr(widgets[0], 'find_all'):
                piece_items = widgets[0].find_all()
                if piece_items:
                    piece_color = widgets[0].itemcget(piece_items[0], 'fill')
                    if piece_color == 'white':
                        pieces_blanches += 1
                        coups, _ = calcul_coups_possibles(i, j)
                        if coups:
                            mouvements_blancs = True
                    else:
                        pieces_noires += 1
                        coups, _ = calcul_coups_possibles(i, j)
                        if coups:
                            mouvements_noirs = True
    
    # Vérifie les conditions de victoire
    if pieces_blanches == 0 or (not mouvements_blancs and tour_blanc):
        return "noirs"
    elif pieces_noires == 0 or (not mouvements_noirs and not tour_blanc):
        return "blancs"
    return None

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("Jeu de dames")
fenetre.state("zoomed")
fenetre.iconbitmap("dames.ico")

# Créer un cadre principal pour organiser tous les éléments
cadre_principal = Frame(fenetre)
cadre_principal.pack(fill=BOTH)

# Titre en haut
titre = Label(cadre_principal, text="JEU DE DAMES", font=('Arial', 24, 'bold'), pady=20)
titre.pack()

# Créer un cadre horizontal pour le damier et le bouton
cadre_horizontal = Frame(cadre_principal)
cadre_horizontal.pack() 

# Créer un cadre pour contenir le damier et le message de tour
cadre_jeu = Frame(cadre_horizontal)
cadre_jeu.pack(side=LEFT, padx=20)

# Créer un cadre pour le bouton retour
cadre_boutons = Frame(cadre_horizontal)
cadre_boutons.pack(side=LEFT, padx=20)

def retour_menu():
    # Fonction à implémenter pour retourner au menu
    fenetre.destroy()  # Pour l'instant, on ferme juste la fenêtre

# Bouton retour au menu
bouton_retour = Button(cadre_boutons, text="Retour au menu", 
                      font=('Arial', 12), 
                      command=retour_menu,
                      pady=10,
                      padx=20,
                      bg='lightgray')
bouton_retour.pack()

creer_damier()
placer_pions_initiaux()
Label(cadre_jeu, text="Tour des blancs", bg='white').grid(row=8, column=0, columnspan=8)

fenetre.mainloop()