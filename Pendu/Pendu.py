

class Pendu():
    """Cette classe gère un jeu de pendu (base sans affichage)"""
    
    def __init__(self,word,max_guesses):
        self.word = word
        self.left_guesses = max_guesses
        self.max_guesses = max_guesses
        #faire plus simple
        self.word_dict = {self.word[i]: False for i in range(len(self.word))}

    def check_letter(self, letter):
        """Contrôle si la lettre est présente dans le mot, décrémente le nombre d'essaie si nécéssaire"""
        if len(letter) is 1 and self.left_guesses > 0:
            if letter in self.word:
                self.word_dict[letter] = True
            else:
                self.left_guesses -= 1

    def is_game_won(self):
        for key, value in self.word_dict.items():
            if not value:
                return False
        return True




if __name__ == "__main__":
    pendu = Pendu("travis",10)
    while pendu.left_guesses > 0 and not pendu.is_game_won():
        user_in = input("Entrer une lettre : ")
        pendu.check_letter(user_in)
        board = pendu.word_dict
        out = ""
        for letter in pendu.word:
            if board[letter]:
                out += letter +" "
            else:
                out += " _ "
        print(out)
    if pendu.is_game_won():
        print("Bravo ! Vous avez gagné !")
    else:
        print("Dommage :( peut-être une prochaine fois")
