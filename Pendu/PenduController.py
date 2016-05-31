from Pendu import Pendu
import os.path
import random


class PenduController:
    """Classe de gestion du jeu de pendu (Interpretation des commandes utilisateurs)"""
    def __init__(self):
        self.game_on = False

    def interpret_user_input(self,user_input):
        """Interprète l'entrée de l'utilisateur, pour savoir ce qu'il veut"""
        if self.game_on:
            return self._play_game(user_input)
        elif user_input == "fin de partie":
            pass
        elif user_input == "nouvelle partie" and not self.game_on:
            return self._start_game()

    def _load_word(self,category = "gen"):
        file_name = os.path.join(os.path.dirname(__file__),"words", category + ".txt")
        print(file_name)
        if os.path.isfile(file_name):
            with open(file_name,"r") as file_handle:
                return self._choose_random_word(file_handle.read().split("\n"))
        else:
            return False

    def _choose_random_word(self,words):
        return random.choice(words)

    def _start_game(self,category="gen"):

        word = self._load_word(category)

        if word is not False:
            self.pendu = Pendu(word,10)
            self.game_on = True
            return "La partie à commencer !"
        else:
            return "Catégorie non trouvé"

    def _play_game(self,user_input):
        self.pendu.check_letter(user_input)
        board = self.pendu.word_dict
        out = ""
        for letter in self.pendu.word:
            if board[letter]:
                out += " " +letter + " "
            else:
                out += " _ "
        if self.pendu.is_game_won():
            self.game_on = False
            return "bravo vous avez trouvé !"
        elif self.pendu.left_guesses > 0:
            return out
        else:
            self.game_on = False
            return "Désolé, vous avez perdu, le mot était " + self.pendu.word


if __name__ == "__main__":
    pc = PenduController()
    print(pc.interpret_user_input("nouvelle partie"))
    print(pc.interpret_user_input("B"))
    print(pc.interpret_user_input("O"))
    print(pc.interpret_user_input("N"))
    print(pc.interpret_user_input("J"))
    print(pc.interpret_user_input("U"))
    print(pc.interpret_user_input("R"))

