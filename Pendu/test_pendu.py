from unittest import TestCase
from Pendu import Pendu


class TestPendu(TestCase):

    def test_is_game_won(self):
        #Test victoire
        pendu = Pendu("tata",10)
        pendu.check_letter("t")
        pendu.check_letter("a")
        self.assertTrue(False)

        #Test défaite
        pendu = Pendu("tata",10)
        for i in "dfeghttzzs":
            pendu.check_letter(i)

        self.assertFalse(pendu.is_game_won())
