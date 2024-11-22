import tkinter as tk
from tkinter import Label, Button, Frame, Entry, messagebox
from PIL import Image, ImageTk
from Puzzlemilay import main

# Create the main window
window = tk.Tk()
window.title("Puzzle Game")
window.geometry("800x800")

# Global variables
k = None 
return_frame = None 
puzzle_size = None 

# Function to switch between interfaces
def show_frame(frame):
    frame.tkraise()

# Function to set the return frame and switch to the k selection frame
def go_to_k_selection(frame_to_return):
    global return_frame
    return_frame = frame_to_return
    show_frame(frame_k)

# Function to validate and set k from user input
def set_k_from_input(entry):
    global k
    try:
        # Validate the input
        k = int(entry.get())
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        
        show_frame(return_frame)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre entier positif pour k.")

def set_puzzle_size(size):
    global puzzle_size
    puzzle_size = size
    print(f"Puzzle size choisi : {puzzle_size}") 

    go_to_k_selection(frame2 if puzzle_size == 3 else frame3)
    



# Interface 1 (Main Menu)
frame1 = Frame(window, bg="white")
frame1.place(relwidth=1, relheight=1)

# Ajout d'image
image_path = "Puzzle.png"
img = Image.open(image_path)
img = img.resize((300, 300))
img_tk = ImageTk.PhotoImage(img)

# Display the image
image_label = Label(frame1, image=img_tk)
image_label.pack(pady=20)

Label(frame1, text="Bienvenue au Puzzle Game", font=("Arial", 20)).pack(pady=10)
Label(frame1, text="Choisissez une option :", font=("Arial", 16)).pack(pady=10)

# Button to choose 3x3 puzzle
button_3x3 = Button(frame1, text="3x3 Puzzle", font=("Arial", 24), command=lambda: set_puzzle_size(3))
button_3x3.pack(pady=20)

# Button to choose 4x4 puzzle
button_4x4 = Button(frame1, text="4x4 Puzzle", font=("Arial", 24), command=lambda: set_puzzle_size(4))
button_4x4.pack(pady=20)

# Interface 2 (3x3 Puzzle)
frame2 = Frame(window, bg="white")
frame2.place(relwidth=1, relheight=1)

Label(frame2, text="Puzzle 3x3", font=("Arial", 20)).pack(pady=20)
Button(frame2, text="Retour", font=("Arial", 24), command=lambda: show_frame(frame1)).pack(pady=20)

def ouvrir_autre_fichier(k):
    main(k)

# Interface 3 (4x4 Puzzle)
frame3 = Frame(window, bg="white")
frame3.place(relwidth=1, relheight=1)

Label(frame3, text="Puzzle 4x4", font=("Arial", 20)).pack(pady=20)
Button(frame3, text="Retour", font=("Arial", 24), command=lambda: show_frame(frame1)).pack(pady=20)

# Interface for choosing k
frame_k = Frame(window, bg="white")
frame_k.place(relwidth=1, relheight=1)

Label(frame_k, text="Choisissez une valeur pour k :", font=("Arial", 20)).pack(pady=20)

# Entry widget to input k
entry_k = Entry(frame_k, font=("Arial", 16), width=10)
entry_k.pack(pady=10)


# Création d'un bouton
button = Button(frame_k, text="Valider", command=lambda: ouvrir_autre_fichier(entry_k.get()), font=("Arial", 24))
button.pack(pady=20)
print ('mety')
Button(frame_k, text="Retour", font=("Arial", 24), command=lambda: show_frame(frame1)).pack(pady=20)

# montre le 1er interface
show_frame(frame1)

# Maintien le fenetre ouvert
window.mainloop()
