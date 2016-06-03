

class Pendu():
    """Cette classe gère un jeu de pendu (base sans affichage)"""
    
    def __init__(self,word,max_guesses):
        self.word = word
        self.left_guesses = max_guesses
        self.max_guesses = max_guesses
        self.guesses = set()

    def check_letter(self, letter):
        if letter not in self.guesses:
            self.guesses.add(letter)

    def check_word(self,word):
        if word == self.word:
            return True
        else:
            self.left_guesses -= 1
            return False

    def is_game_won(self):
        return len(set(self.word) - self.guesses) == 0

    def show(self):
        out = []
        for w in self.word:
            if w in self.guesses:
                out.append(" {0} ".format(w))
            else:
                out.append(" ˽ ")
        return ''.join(out)

    @property
    def nb_guesses(self):
        return self.max_guesses - self.nb_false_tries

    @property
    def nb_false_tries(self):
        return len(self.guesses - set(self.word))


if __name__ == "__main__":
    pendu = Pendu("travis",10)
    while pendu.nb_guesses > 0 and not pendu.is_game_won():
        user_in = input("Entrer une lettre : ")
        pendu.check_letter(user_in)
        print(pendu.show())
        print("il vous reste " + str(pendu.nb_guesses))
    if pendu.is_game_won():
        print("Bravo ! Vous avez gagné !")
    else:
        print("Dommage :( peut-être une prochaine fois")
