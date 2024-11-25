import tkinter as tk
from tkinter import Label, Button, Frame, Entry, messagebox
from PIL import Image, ImageTk

# Fenêtre principale
window = tk.Tk()
window.title("Puzzle Game")
window.geometry("800x800")

# Variables globales
puzzle_size = None  # Taille du puzzle (3 ou 4)
k = None  # Nombre de déplacements avant swap
return_frame = None 

# Fonction pour changer d'interface
def show_frame(frame):
    frame.tkraise()

# Valider la taille du puzzle
def set_puzzle_size(size):
    global puzzle_size
    puzzle_size = size
    print(f"Taille du puzzle : {puzzle_size}")
    show_frame(frame_k)

# Valider k
def set_k_from_input(entry):
    global k
    try:
        k = int(entry.get())
        if k <= 0:
            raise ValueError("k doit être un entier positif.")
        print(f"Valeur de k : {k}")
        start_game()
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un entier positif.")

# Démarrer le jeu
def start_game():
    if puzzle_size is None or k is None:
        messagebox.showerror("Erreur", "Veuillez définir la taille du puzzle et la valeur de k.")
        return

    try:
        from Puzzlemilay import main
        main(puzzle_size, k)  # Passer les paramètres au jeu
    except ImportError as e:
        messagebox.showerror("Erreur", f"Impossible de charger le jeu : {e}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Charger l'image d'arrière-plan
try:
    bg_image_path = "Puzzle.png"  
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((325, 325))  
    bg_image_tk = ImageTk.PhotoImage(bg_image)
except Exception as e:
    messagebox.showerror("Erreur", f"Impossible de charger l'image d'arrière-plan : {e}")
    bg_image_tk = None

# Interface principale
frame_main = Frame(window, bg="white")
frame_main.place(relwidth=1, relheight=1)

# Ajouter une section pour l'image
frame_image_main = Frame(frame_main, bg="white")
frame_image_main.pack(pady=50)  # Ajustez `pady` pour modifier la hauteur de l'image

if bg_image_tk:
    bg_label_main = Label(frame_image_main, image=bg_image_tk, bg="white")
    bg_label_main.pack()

# Ajouter les widgets au-dessus ou en dessous de l'image
Label(frame_main, text="Bienvenue au Puzzle Game", font=("Arial", 20), bg="white").pack(pady=10)
Label(frame_main, text="Choisissez une option", font=("Arial", 16), bg="white").pack(pady=20)
Button(frame_main, text="3x3 Puzzle", font=("Arial", 20), command=lambda: set_puzzle_size(3)).pack(pady=10)
Button(frame_main, text="4x4 Puzzle", font=("Arial", 20), command=lambda: set_puzzle_size(4)).pack(pady=10)

# Interface pour choisir k
frame_k = Frame(window, bg="white")
frame_k.place(relwidth=1, relheight=1)

# Ajouter une section pour l'image
frame_image_k = Frame(frame_k, bg="white")
frame_image_k.pack(pady=50)  # Ajustez `pady` pour modifier la hauteur de l'image

if bg_image_tk:
    bg_label_k = Label(frame_image_k, image=bg_image_tk, bg="white")
    bg_label_k.pack()

# Ajouter les widgets au-dessus ou en dessous de l'image
Label(frame_k, text="Entrez une valeur pour k :", font=("Arial", 20), bg="white").pack(pady=20)
entry_k = Entry(frame_k, font=("Arial", 16), width=10)
entry_k.pack(pady=10)
Button(frame_k, text="Valider", font=("Arial", 20), command=lambda: set_k_from_input(entry_k)).pack(pady=10)
Button(frame_k, text="Retour", font=("Arial", 20), command=lambda: show_frame(frame_main)).pack(pady=10)


# Montrer l'interface principale
show_frame(frame_main)

# Boucle principale
window.mainloop()
