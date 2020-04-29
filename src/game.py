"""Игра 'Пятнашки'"""

import sys
import random

import pygame

class Game15:
    TITLE = 'Пятнашки'

    DEFAULT_SIDE_SIZE = 4
    SIZE = WIDTH, HEIGTH = 400, 400
    BORDER_WIDTH = 5
    BLACK = 0, 0, 0
    GRAY = 136, 136, 136
    WHITE = 220, 220, 220

    screen = None
    __click_count = 0

    def __init__(self, side_size=DEFAULT_SIDE_SIZE):
        self.__set_options(side_size)

        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.my_font = pygame.font.SysFont('monospace', 48)

    def __del__(self):
        print(self.__l_board)

    def __set_options(self, side_size):
        self.side_size = side_size if 2 <= side_size <= 10 else self.DEFAULT_SIDE_SIZE
        self.dice_count = self.side_size ** 2
        self.rect_size = self.WIDTH / self.side_size

    def start(self):
        self.screen = pygame.display.set_mode(self.SIZE)
        self.__l_board = board = Game15.__generate_board(self.dice_count)
        self.__render(board)
        self.__process(board)

    def __process(self, board):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            is_clicked, *q = pygame.mouse.get_pressed()

            if is_clicked:
                self.__move_dice(board)

    def __move_dice(self, board):
        """Перемещение фишки по полю"""
        x, y = pygame.mouse.get_pos()
        i = int(x / self.rect_size)
        j = int(y / self.rect_size)
        pos = j*self.side_size+i
        n = board[pos]

        if n != self.dice_count:
            empty_pos = board.index(self.dice_count)
            if empty_pos in [pos-1, pos+1, pos+self.side_size, pos-self.side_size]:
                self.__click_count += 1
                board[empty_pos], board[pos] = board[pos], board[empty_pos]
                self.__render(board)
                if self.__is_win(board):
                    self.__draw_win()

    @staticmethod
    def is_solvable_board(board):
        """Проверяем, что сгенерированный набор фишек - решаем

        Определяем "Четность расклада",
        для досок с четным количеством полей - она должна сойтись,
        для досок с нечетным количеством полей - разойтись.
        """
        last = []
        total = 0
        pos = -1
        for point in board:
            pos = pos + 1
            if point == len(board):
                total = total + int(pos / (len(board) ** .5)) + 1
            else:
                last.append(point)
                for p in range(1, point):
                    if p not in last:
                        total = total + 1
        # сравнение "Четности расклада"
        return total % 2 == len(board) % 2

    @classmethod
    def __generate_board(cls, dice_count):
        """Генерация фишек"""
        board = list(range(1, dice_count + 1))
        random.shuffle(board)
        return board if cls.is_solvable_board(board) else cls.__generate_board(dice_count)

    def __render(self, board):
        self.screen.fill(self.BLACK)

        pos = -1
        for n in board:
            pos = pos + 1
            j = int(pos / self.side_size)
            i = pos % self.side_size

            # пустое место на доске - пропускаем
            if n == self.dice_count:
                continue

            # координаты верхнего левого угла фишки с учетом отрисовки граней
            x = self.rect_size * i + self.BORDER_WIDTH
            y = self.rect_size * j + self.BORDER_WIDTH
            # размеры фишки с учетом отрисовки граней
            width  = self.rect_size - self.BORDER_WIDTH * (2 if i == self.side_size - 1 else 1)
            height = self.rect_size - self.BORDER_WIDTH * (2 if j == self.side_size - 1 else 1)
            # отрисовка фишки
            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.screen, self.GRAY, rect)
            # отрисовки надписи на фишке
            label = self.my_font.render(str(n), 1, (self.WHITE))
            self.screen.blit(label, (x + width/2 - label.get_width()/2, y + height/2 - label.get_height()/2))

        pygame.display.flip()

    @staticmethod
    def __is_win(board):
        for i in range(1, len(board) + 1):
            if i != board[i-1]:
                return False

        return True

    def __draw_win(self):
        color = 220, 10, 10

        label = pygame.font.SysFont('monospace', 82).render('WIN', 1, color)
        self.screen.blit(label, (self.WIDTH/2 - label.get_width()/2, self.HEIGTH/2 - label.get_height()/2))

        label = pygame.font.SysFont('monospace', 20).render('number of moves: {}'.format(self.__click_count), 1, color)
        self.screen.blit(label, (self.WIDTH/2 - label.get_width()/2, self.HEIGTH - self.HEIGTH/4 - label.get_height()/2))

        pygame.display.flip()
