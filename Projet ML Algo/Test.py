import tkinter as tk
from tkinter import Label, Button, Frame, Entry, messagebox
from PIL import Image, ImageTk
import Puzzlemilay  # Assurez-vous que ce module est disponible

# Créer la fenêtre principale
window = tk.Tk()
window.title("Puzzle Game")
window.geometry("800x800")

# Variables globales
k = None 
return_frame = None 
puzzle_size = None 

# Fonction pour changer d'interface
def show_frame(frame):
    frame.tkraise()

# Fonction pour valider et définir k à partir de l'input de l'utilisateur
def go_to_k_selection(frame_to_return):
    global return_frame
    return_frame = frame_to_return
    show_frame(frame_k)

def set_k_from_input(entry):
    global k
    try:
        # Valider l'input
        k = int(entry.get())
        if k <= 0:
            raise ValueError("k doit être un entier positif.")
        
        # Appel de la fonction pour ouvrir Puzzlemilay après validation
        ouvrir_autre_fichier()
        
        # Fermer l'interface de saisie de k et revenir à l'écran principal
        show_frame(return_frame)
        
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif pour k.")

def set_puzzle_size(size):
    global puzzle_size
    puzzle_size = size
    print(f"Taille du puzzle choisie : {puzzle_size}") 

    go_to_k_selection(frame2 if puzzle_size == 3 else frame3)

def ouvrir_autre_fichier():
    donnees = "Message à envoyer à Puzzlemilay"  # Exemple de données à envoyer
    Puzzlemilay.k(donnees)  # Appeler la fonction depuis Puzzlemilay


# Interface 1 (Menu principal)
frame1 = Frame(window, bg="white")
frame1.place(relwidth=1, relheight=1)

# Ajout d'image
image_path = "Puzzle.png"
img = Image.open(image_path)
img = img.resize((300, 300))
img_tk = ImageTk.PhotoImage(img)

# Affichage de l'image
image_label = Label(frame1, image=img_tk)
image_label.pack(pady=20)

Label(frame1, text="Bienvenue au Puzzle Game", font=("Arial", 20)).pack(pady=10)
Label(frame1, text="Choisissez une option :", font=("Arial", 16)).pack(pady=10)

# Bouton pour choisir le puzzle 3x3
button_3x3 = Button(frame1, text="3x3 Puzzle", font=("Arial", 24), command=lambda: set_puzzle_size(3))
button_3x3.pack(pady=20)

# Bouton pour choisir le puzzle 4x4
button_4x4 = Button(frame1, text="4x4 Puzzle", font=("Arial", 24), command=lambda: set_puzzle_size(4))
button_4x4.pack(pady=20)

# Interface 2 (Puzzle 3x3)
frame2 = Frame(window, bg="white")
frame2.place(relwidth=1, relheight=1)

Label(frame2, text="Puzzle 3x3", font=("Arial", 20)).pack(pady=20)
Button(frame2, text="Retour", font=("Arial", 24), command=lambda: show_frame(frame1)).pack(pady=20)

# Grid pour 3x3
canvas_3x3 = tk.Canvas(frame2, width=600, height=600, bg="white")
canvas_3x3.pack()
for i in range(3):
    for j in range(3):
        canvas_3x3.create_rectangle(
            i * 200, j * 200, (i + 1) * 200, (j + 1) * 200, fill="#87ABBE", outline="black"
        )

# Interface 3 (Puzzle 4x4)
frame3 = Frame(window, bg="white")
frame3.place(relwidth=1, relheight=1)

Label(frame3, text="Puzzle 4x4", font=("Arial", 20)).pack(pady=20)
Button(frame3, text="Retour", font=("Arial", 24), command=lambda: show_frame(frame1)).pack(pady=20)

# Grid pour 4x4
canvas_4x4 = tk.Canvas(frame3, width=600, height=600, bg="white")
canvas_4x4.pack()
for i in range(4):
    for j in range(4):
        canvas_4x4.create_rectangle(
            i * 150, j * 150, (i + 1) * 150, (j + 1) * 150, fill="#87ABBE", outline="black"
        )

# Interface pour choisir k
frame_k = Frame(window, bg="white")
frame_k.place(relwidth=1, relheight=1)

Label(frame_k, text="Choisissez une valeur pour k :", font=("Arial", 20)).pack(pady=20)

# Entry pour saisir k
entry_k = Entry(frame_k, font=("Arial", 16), width=10)
entry_k.pack(pady=10)

Button(frame_k, text="Valider", font=("Arial", 24), command=lambda: set_k_from_input(entry_k)).pack(pady=20)
Button(frame_k, text="Retour", font=("Arial", 24), command=lambda: show_frame(frame1)).pack(pady=20)

# Montrer la première interface
show_frame(frame1)

# Maintenir la fenêtre ouverte
window.mainloop()
