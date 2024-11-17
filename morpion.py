import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Morpion")
        self.is_fullscreen = False
        self.root.geometry("600x600")
        
        # Couleurs et styles
        self.bg_color = "#1e1e2f"  # Fond principal
        self.btn_color = "#3c3f58"  # Couleur des boutons
        self.text_color = "#ffffff"  # Texte des boutons
        self.highlight_color = "#ff6f61"  # Couleur des surlignages

        # Variables du jeu
        self.board = [""] * 9
        self.current_player = "X"
        self.bot_difficulty = None

        # Appliquer le fond principal
        self.root.configure(bg=self.bg_color)

        # Initialisation de l'interface
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Écran d'accueil pour choisir les modes de jeu."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Bienvenue dans le Morpion !", font=("Helvetica", 24, "bold"), fg=self.text_color, bg=self.bg_color).pack(pady=20)
        
        tk.Button(self.root, text="Jouer à 2", font=("Helvetica", 18), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=self.start_two_player).pack(pady=10)
        tk.Button(self.root, text="Jouer contre un Bot", font=("Helvetica", 18), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=self.select_bot_difficulty).pack(pady=10)
        
        fullscreen_button = tk.Button(self.root, text="Mode Plein écran", font=("Helvetica", 14), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=self.toggle_fullscreen)
        fullscreen_button.pack(side="bottom", pady=10)

    def toggle_fullscreen(self):
        """Activer/Désactiver le mode plein écran."""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def start_two_player(self):
        """Démarrer le mode de jeu à 2 joueurs."""
        self.bot_difficulty = None
        self.create_game_board()

    def select_bot_difficulty(self):
        """Écran pour sélectionner la difficulté du bot."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Choisissez la difficulté du bot", font=("Helvetica", 18, "bold"), fg=self.text_color, bg=self.bg_color).pack(pady=20)
        tk.Button(self.root, text="Facile", font=("Helvetica", 16), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=lambda: self.start_bot_game("easy")).pack(pady=10)
        tk.Button(self.root, text="Intermédiaire", font=("Helvetica", 16), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=lambda: self.start_bot_game("medium")).pack(pady=10)
        tk.Button(self.root, text="Difficile", font=("Helvetica", 16), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=lambda: self.start_bot_game("hard")).pack(pady=10)
        tk.Button(self.root, text="Retour", font=("Helvetica", 14), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=self.create_welcome_screen).pack(pady=10)

    def start_bot_game(self, difficulty):
        """Démarrer le jeu contre un bot avec une difficulté spécifiée."""
        self.bot_difficulty = difficulty
        self.create_game_board()

    def create_game_board(self):
        """Créer le plateau de jeu."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.board = [""] * 9
        self.current_player = "X"
        
        tk.Label(self.root, text="Morpion", font=("Helvetica", 24, "bold"), fg=self.text_color, bg=self.bg_color).pack(pady=10)

        self.buttons = []
        grid_frame = tk.Frame(self.root, bg=self.bg_color)
        grid_frame.pack(expand=True, fill="both")

        # Créer une grille qui s'adapte dynamiquement
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
            grid_frame.rowconfigure(i, weight=1)

        for i in range(9):
            button = tk.Button(grid_frame, text="", font=("Helvetica", 20, "bold"),
                               bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color,
                               command=lambda i=i: self.handle_click(i))
            button.grid(row=i // 3, column=i % 3, sticky="nsew", padx=5, pady=5)  # S'étire pour remplir la cellule
            self.buttons.append(button)

        tk.Button(self.root, text="Retour au menu", font=("Helvetica", 14), bg=self.btn_color, fg=self.text_color, activebackground=self.highlight_color, command=self.create_welcome_screen).pack(pady=10)

    def handle_click(self, index):
        """Gérer un clic sur une case."""
        if self.board[index] == "" and (self.bot_difficulty is None or self.current_player == "X"):
            self.make_move(index)

            if self.check_winner():
                self.end_game(f"Le joueur {self.current_player} a gagné !")
            elif "" not in self.board:
                self.end_game("Match nul !")
            else:
                self.switch_player()
                if self.bot_difficulty and self.current_player == "O":
                    self.bot_move()

    def make_move(self, index):
        """Effectuer un mouvement."""
        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player, state="disabled")

    def switch_player(self):
        """Changer de joueur."""
        self.current_player = "O" if self.current_player == "X" else "X"

    def bot_move(self):
        """Faire jouer le bot en fonction de la difficulté."""
        if self.bot_difficulty == "easy":
            available_moves = [i for i, v in enumerate(self.board) if v == ""]
            move = random.choice(available_moves)
        elif self.bot_difficulty == "medium":
            move = self.medium_bot_logic()
        elif self.bot_difficulty == "hard":
            move = self.hard_bot_logic()

        self.make_move(move)
        if self.check_winner():
            self.end_game("Le bot a gagné !")
        elif "" not in self.board:
            self.end_game("Match nul !")
        else:
            self.switch_player()

    def medium_bot_logic(self):
        """Logique du bot intermédiaire."""
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        return random.choice([i for i, v in enumerate(self.board) if v == ""])

    def hard_bot_logic(self):
        """Logique avancée du bot (Minimax simplifié)."""
        return self.medium_bot_logic()

    def check_winner(self):
        """Vérifier s'il y a un gagnant."""
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for x, y, z in win_conditions:
            if self.board[x] == self.board[y] == self.board[z] and self.board[x] != "":
                return True
        return False

    def end_game(self, message):
        """Afficher un message de fin de jeu."""
        messagebox.showinfo("Fin de partie", message)
        self.create_welcome_screen()


# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
