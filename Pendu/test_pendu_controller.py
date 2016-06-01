from unittest import TestCase
from PenduController import PenduController


class TestPenduController(TestCase):

    def test_normal_game(self):
        pc = PenduController("BONJOUR")
        self.assertEquals("La partie a commencé !",pc.interpret_user_input("nouvelle partie"))
        self.assertEquals(" B  ˽  ˽  ˽  ˽  ˽  ˽ ", pc.interpret_user_input("B"))
        self.assertEquals(" B  O  ˽  ˽  O  ˽  ˽ ", pc.interpret_user_input("O"))
        self.assertEquals(" B  O  N  ˽  O  ˽  ˽ ", pc.interpret_user_input("N"))
        self.assertEquals(" B  O  N  J  O  ˽  ˽ ", pc.interpret_user_input("J"))
        self.assertEquals(" B  O  N  J  O  U  ˽ ", pc.interpret_user_input("U"))
        self.assertEquals("bravo vous avez trouvé !", pc.interpret_user_input("R"))

