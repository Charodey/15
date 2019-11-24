"""Игра 'Пятнашки'"""

import sys
import random

import pygame

class Game15:
    TITLE = 'Пятнашки'

    SIZE = WIDTH, HEIGTH = 400, 400
    BORDER_WIDTH = 5
    BLACK = 0, 0, 0

    def __init__(self, side_size=4):
        self.__set_options(side_size)

        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.my_font = pygame.font.SysFont('monospace', 48)

    def __set_options(self, side_size):
        self.side_size = side_size
        self.dice_count = side_size ** 2
        self.rect_size = self.WIDTH / side_size

    def start(self):
        screen = pygame.display.set_mode(self.SIZE)
        board = self.__generate_board()
        self.render(screen, board)
        self.__process(screen, board)

    def __process(self, screen, board):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            is_clicked, *q = pygame.mouse.get_pressed()

            if is_clicked:
                self.__move_dice(screen, board)

    def __move_dice(self, screen, board):
        """Перемещение фишки по полю"""
        x, y = pygame.mouse.get_pos()
        i = int(x / self.rect_size)
        j = int(y / self.rect_size)
        pos = j*self.side_size+i
        n = board[pos]

        if n != self.dice_count:
            empty_pos = board.index(self.dice_count)
            if empty_pos in [pos-1, pos+1, pos+self.side_size, pos-self.side_size]:
                board[empty_pos], board[pos] = board[pos], board[empty_pos]
                self.render(screen, board)
                self.check_win(screen, board)

    def check_board(self, board):
        """Проверяем, что сгенерированный набор фишек - решаем"""

        # todo: ! не работает для поля 3x3
        last = []
        total = 0
        pos = -1
        for point in board:
            pos = pos + 1
            if point == self.dice_count:
                total = total + int(pos / self.side_size) + 1
            else:
                last.append(point)
                for p in range(1, point):
                    if p not in last:
                        total = total + 1

        return total % 2 == 0

    def __generate_board(self):
        """Генерация фишек"""
        board = list(range(1, self.dice_count + 1))
        random.shuffle(board)
        return board if self.check_board(board) else self.__generate_board()

    def render(self, screen, board):
        screen.fill(self.BLACK)

        pos = -1
        for n in board:
            pos = pos + 1
            j = int(pos / self.side_size)
            i = pos % self.side_size

            if n == self.dice_count:
                continue

            x = self.rect_size * i + self.BORDER_WIDTH
            y = self.rect_size * j + self.BORDER_WIDTH
            width = self.rect_size - self.BORDER_WIDTH * (2 if i == 3 else 1)
            height = self.rect_size - self.BORDER_WIDTH * (2 if j == 3 else 1)

            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(screen, [136, 136, 136], rect)

            label = self.my_font.render(str(n), 1, (220, 220, 220))
            screen.blit(label, (x + width/2 - label.get_width()/2, y + height/2 - label.get_height()/2))

        pygame.display.flip()

    def check_win(self, screen, board):
        for i in range(1, self.dice_count + 1):
            if i != board[i-1]:
                break
            if i == self.dice_count:
                label = pygame.font.SysFont('monospace', 82).render('WIN', 1, (220, 10, 10))
                screen.blit(label, (self.WIDTH/2 - label.get_width()/2, self.HEIGTH/2 - label.get_height()/2))
                pygame.display.flip()
