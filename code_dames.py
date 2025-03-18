from tkinter import *

def placer_piece(row, col, piece):
    piece.grid(row=row, column=col)
    return piece

def placer_bouton(row, col, bouton):
    bouton.grid(row=row, column=col)
    return bouton

def click_pion(row, col):
    print(f"Pion en {row},{col} cliqué")
    # Logique du jeu ici

fenetre = Tk()
fenetre.title("Jeu de dames")
fenetre.geometry("1000x750")
fenetre.resizable(width=False, height=False)

# On créé le damier
for i in range(8):
    for j in range(8):
        frame = Frame(fenetre, width=80, height=80, bg='white' if (i+j)%2==0 else 'black')
        frame.grid(row=i, column=j)


# On place les pièces
for j in range (3):
    for i in range(0,7,2):
        pion_blanc = Canvas(fenetre, width=80, height=80, bg='white')
        pion_blanc.create_oval(10, 10, 70, 70, fill='white', outline='black', width=2)
        placer_piece(j, i, pion_blanc) if j%2==0 else placer_piece(j, i+1, pion_blanc)
    for k in range(1,8,2):
        pion_noir = Canvas(fenetre, width=80, height=80, bg='white')
        pion_noir.create_oval(10, 10, 70, 70, fill='black', outline='white', width=2)
        pion_noir.bind('<Button-1>', lambda: click_pion(7-j, k))
        placer_piece(7-j, k, pion_noir) if j%2==0 else placer_piece(7-j, k-1, pion_noir)
        

fenetre.mainloop()