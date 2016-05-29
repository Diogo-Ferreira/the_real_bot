from unittest import TestCase
from PenduController import PenduController


class TestPenduController(TestCase):

    def test_normal_game(self):
        pc = PenduController()
        self.assertEquals("La partie à commencer !",pc.interpret_user_input("nouvelle partie"))
        self.assertEquals(" B  _  _  _  _  _  _ ", pc.interpret_user_input("B"))
        self.assertEquals(" B  O  _  _  O  _  _ ", pc.interpret_user_input("O"))
        self.assertEquals(" B  O  N  _  O  _  _ ", pc.interpret_user_input("N"))
        self.assertEquals(" B  O  N  J  O  _  _ ", pc.interpret_user_input("J"))
        self.assertEquals(" B  O  N  J  O  U  _ ", pc.interpret_user_input("U"))
        self.assertEquals("bravo vous avez trouvé !", pc.interpret_user_input("R"))

