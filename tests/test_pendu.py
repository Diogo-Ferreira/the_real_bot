from unittest import TestCase
from Pendu import Pendu


class TestPendu(TestCase):

    def test_is_game_won(self):
        #Test victoire
        pendu = Pendu("tata",10)
        pendu.check_letter("t")
        pendu.check_letter("a")
        self.assertTrue(pendu.is_game_won())

        #Test défaite
        pendu = Pendu("tata",10)
        for i in "dfeghttzzs":
            pendu.check_letter(i)

        self.assertFalse(pendu.is_game_won())

    def test_max_guess_not_decremented_after_good_guess(self):
        pendu = Pendu("bonjour",12)
        pendu.check_letter("b")
        pendu.check_letter("j")
        self.assertEquals(12,pendu.left_guesses)
