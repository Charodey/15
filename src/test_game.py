import unittest
import random

from game import Game15


class TestGame(unittest.TestCase):

    def test_is_solvable_board(self):
        """Число решаемых наборов фишек при случайной генерации должно составлять ~50%"""
        for side_size in range(2, 9):
            game = Game15(side_size)

            i = 0
            cnt = 1000
            cnt_true = 0
            board = list(range(1, side_size ** 2 + 1))
            while i < 1000:
                random.shuffle(board)
                cnt_true = cnt_true + (1 if game.is_solvable_board(board) else 0)
                i = i + 1

            cnt_true_percent = cnt_true / cnt * 100
            self.assertTrue(45 < cnt_true_percent < 55)

    def test_is_solvable_board_predefined(self):
        """Проверка решаемости комбинаций

        Если у решаемой комбинации фишек поменять местами 2 последовательных элемента,
        то комбинация станет нерешаемой

        """
        for side_size in range(2, 11):
            board_count = side_size ** 2

            game = Game15(side_size)
            # решаемая комбинация
            board = list(range(1, board_count + 1))
            self.assertTrue(game.is_solvable_board(board))
            # нерешаемая комбинация
            board[board_count - 3], board[board_count - 2] = board[board_count - 2], board[board_count - 3]
            self.assertFalse(game.is_solvable_board(board))


if __name__ == '__main__':
    unittest.main()
