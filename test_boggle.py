from unittest import TestCase
from boggle import Boggle

test_game = Boggle()
test_game.board = test_game.make_board()
test_game.board[2] = ['F', 'I', 'X', 'E', 'D']

class CheckValidWordTestCase(TestCase):
    """ Checks that function correctly assigns result to word guess. """
    def test_check_valid_word(self):
        should_be_ok = test_game.check_valid_word(test_game.board, 'fixed')
        should_be_notonboard = test_game.check_valid_word(test_game.board, 'water')
        should_be_notword = test_game.check_valid_word(test_game.board, 'asdf')
        self.assertEqual(should_be_ok, 'ok')
        self.assertEqual(should_be_notonboard, 'not-on-board')
        self.assertEqual(should_be_notword, 'not-word')