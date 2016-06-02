from Pendu import Pendu
import os.path
import random


class PenduController:
    """Classe de gestion du jeu de pendu (Interpretation des commandes utilisateurs)"""
    def __init__(self,word = None):
        self.game_on = False
        self.word = word

    def interpret_user_input(self,user_input):
        """Interprète l'entrée de l'utilisateur, pour savoir ce qu'il veut"""

        if user_input == "aide moi":
            return "affichage aide..."
        elif user_input == "fin de partie":
            self.game_on = False
            return "Bye Bye"
        elif self.game_on:
            return self._play_game(user_input)
        elif "nouvelle partie" in user_input and not self.game_on:

            #Categorie spécifié ?
            if len(user_input) > len("nouvelle partie"):
                category = user_input.split(" ")[-1]
                return self._start_game(category)
            else:
                return self._start_game()

        else:
            return "je ne te comprends pas, consulte l'aide en m'écrivant \"aide moi\""

    def _load_word(self,category = "gen"):
        file_name = os.path.join(os.path.dirname(__file__),"words", category + ".txt")
        if os.path.isfile(file_name):
            with open(file_name,"r") as file_handle:
                return self._choose_random_word(file_handle.read().split("\n"))
        else:
            return False

    def _choose_random_word(self,words):
        return random.choice(words)

    def _start_game(self,category="gen"):

        if self.word is None:
            self.word = self._load_word(category)

        if self.word is not False:
            self.pendu = Pendu(self.word,10)
            self.game_on = True
            return "La partie a commencé !"
        else:
            return "Catégorie non trouvé"

    def _play_game(self,user_input):

        #Si le joueur devine le mot
        if len(user_input) > 1:
            if user_input == self.pendu.word:
                self.game_on = False
                return "vous avez gagné "
            else:
                self.pendu.left_guesses -= 1
                return "non, ce n'est pas le mot !"

        self.pendu.check_letter(user_input)
        board = self.pendu.word_dict
        out = ""
        for letter in self.pendu.word:
            if board[letter]:
                out += " " +letter + " "
            else:
                out += " ˽ "
        if self.pendu.is_game_won():
            self.game_on = False
            return "bravo vous avez trouvé !"
        elif self.pendu.left_guesses > 0:
            return out
            #+ " il vous reste " + str(self.pendu.left_guesses) + " essaies !"
        else:
            self.game_on = False
            return "Désolé, vous avez perdu, le mot était " + self.pendu.word

    def get_current_image(self):
        if self.game_on:
            return "http://diogoferreira.ch/pendu/" + str(int(self.pendu.max_guesses - self.pendu.left_guesses+1)) + ".png \n"


if __name__ == "__main__":
    pc = PenduController()
    print(pc.interpret_user_input("nouvelle partie"))
    print(pc.interpret_user_input("B"))
    print(pc.interpret_user_input("O"))
    print(pc.interpret_user_input("N"))
    print(pc.interpret_user_input("J"))
    print(pc.interpret_user_input("U"))
    print(pc.interpret_user_input("R"))

