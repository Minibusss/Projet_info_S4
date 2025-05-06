import tkinter as tk
from InterfaceMenu import interface

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Polystation 4")
    root.state("zoomed")  # Fenêtre maximisée avec la croix
    root.config(bg="#FFFFFF")

    # Conteneur central dans lequel on affichera les différents écrans
    main_frame = tk.Frame(root, bg="#FFFFFF")
    main_frame.pack(expand=True, fill=tk.BOTH)

    # Lancer l'interface menu dans ce conteneur
    interface(root, main_frame)

    root.mainloop()
