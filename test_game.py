import unittest
import random

from game import check_board


class TestGame(unittest.TestCase):

    def test_check_board(self):
        '''Число решаемых наборов фишек при случайной генерации должно составлять ~50%'''
        i = 0
        cnt = 1000
        cnt_true = 0
        board = list(range(1, 17))
        while i < 1000:
            random.shuffle(board)
            cnt_true = cnt_true + (1 if check_board(board) else 0)
            i = i + 1

        cnt_true_percent = cnt_true / cnt * 100
        self.assertTrue(45 < cnt_true_percent < 55)

    def test_check_board_predefined(self):
        '''Проверка решаемости комбинаций

        Если у решаемой комбинации фишек поменять местами 2 последовательных элемента,
        то комбинация станет нерешаемой

        '''
        board = list(range(1, 17))
        self.assertTrue(check_board(board))
        board[14] = 14
        board[13] = 15
        self.assertFalse(check_board(board))


if __name__ == '__main__':
    unittest.main()
