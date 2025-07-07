from train import train_model
from game import play_game
from interface import lancer_interface

if __name__ == "__main__":
    print("1. Entraîner le modèle")
    print("2. Lancer le jeu en console")
    print("3. Lancer l'interface graphique")
    choix = input("Choix (1/2/3) : ")
    if choix == "1":
        train_model()
    elif choix == "2":
        play_game()
    elif choix == "3":
        lancer_interface()
    else:
        print("Choix invalide.")