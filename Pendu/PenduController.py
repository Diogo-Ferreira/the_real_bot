from Pendu import Pendu
import os.path
import random


class PenduController:
    """
    Classe de gestion du jeu de pendu (Interpretation
     des commandes utilisateurs depuis slack)
    """
    def __init__(self,word = None):
        self.game_on = False
        self.word = word

    def interpret_user_input(self,user_input):
        """
        Gère le jeu suivant ce que l'utilisateur écrit
        :param user_input: message utilisateur
        :return: réponse à afficher à l'utilisateur
        """
        if user_input == "aide moi":
            return "Pour commencer une partie tapez : nouvelle partie \n" \
                   "Vous pouvez faire suivre cette commande d'une catégorie de votre choix\n" \
                   "Les catégories disponibles sont les suivants : gen (catégorie par défaut)\n" \
                   "Pour terminer une partie tapez : fin de partie\n" \
                   "Une fois que la partie a commencé tapez la lettre de votre choix\n" \
                   "Vous pouvez taper un mot en entier si vous pensez l'avoir devnié."
        elif user_input == "fin de partie":
            self.game_on = False
            return "Bye Bye"
        elif self.game_on:
            return self._play_game(user_input)
        elif "nouvelle partie" in user_input and not self.game_on:

            #Categorie spécifié ?
            if len(user_input) > len("nouvelle partie"):
                #on prends le dernier mot écrit
                category = user_input.split(" ")[-1]
                return self._start_game(category)
            else:
                return self._start_game("gen")

        else:
            return "je ne te comprends pas, consulte l'aide en m'écrivant \"aide moi\""

    def _load_word(self,category):
        """
        Charge une liste de mot dans un fichier
        :param category: catégorie de mots (nom du fichier sans extension)
        :return:
        """
        file_name = os.path.join(os.path.dirname(__file__),"words", "{0}.txt".format(category))
        if os.path.isfile(file_name):
            with open(file_name,"r") as file_handle:
                return self._choose_random_word(file_handle.read().split("\n"))
        else:
            return False

    def _choose_random_word(self,words):
        return random.choice(words)

    def _start_game(self,category):
        """
        Init d'une partie pendu
        :param category: catégorie du mot
        :return: réponse à forwarder à l'utilisateur
        """
        if self.word is None:
            self.word = self._load_word(category)

        if self.word is not False:
            self.pendu = Pendu(self.word, 11)
            self.game_on = True
            return "La partie a commencé !"
        else:
            return "Catégorie non trouvé"

    def _play_game(self, user_input):
        """
        Gestion d'une partie
        :param user_input: message utilisateur
        :return: réponse à forwarder à l'utilisateur
        """

        #Si le joueur devine le mot
        if len(user_input) > 1 and self.pendu.check_word(user_input):
            self.game_on = False
            self.word = None
            return "vous avez gagné !"
        elif len(user_input) > 1:
            return "non, ce n'est pas le mot"

        self.pendu.check_letter(user_input)
        out = self.pendu.show()
        if self.pendu.is_game_won():
            self.game_on = False
            self.word = None
            return "bravo vous avez trouvé !"
        elif self.pendu.nb_guesses > 0:
            return out
        else:
            self.game_on = False
            return "Désolé, vous avez perdu, le mot était {0}".format(self.pendu.word)

    def get_current_image(self):
        """
        Retourne l'image de pendu suivant le nombre d'essaie restant
        :return: url de l'image
        """
        if self.game_on:
            return "http://diogoferreira.ch/pendu/{0}.png".format(self.pendu.nb_false_tries+1)


if __name__ == "__main__":
    pc = PenduController()
    print(pc.interpret_user_input("nouvelle partie"))
    print(pc.interpret_user_input("B"))
    print(pc.interpret_user_input("O"))
    print(pc.interpret_user_input("N"))
    print(pc.interpret_user_input("J"))
    print(pc.interpret_user_input("U"))
    print(pc.interpret_user_input("R"))

