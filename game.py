import sys
import random

import pygame

class Game15:
    DICE_ON_SIDE = 4
    DICE_COUNT = DICE_ON_SIDE ** 2
    SIZE = WIDTH, HEIGTH = 400, 400
    RECT_SIZE = WIDTH / DICE_ON_SIDE

    BORDER_WIDTH = 5
    BLACK = 0, 0, 0

    def __init__(self, dice_on_side=4):
        self.DICE_ON_SIDE = dice_on_side
        self.DICE_COUNT = dice_on_side ** 2
        self.RECT_SIZE = self.WIDTH / dice_on_side

        pygame.init()
        pygame.display.set_caption("Пятнашки")
        self.MY_FONT = pygame.font.SysFont("monospace", 48)

    def start(self):
        screen = pygame.display.set_mode(self.SIZE)
        board = self.__generate_board()
        self.render(screen, board)
        self.__process(screen, board)

    def __process(self, screen, board):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            is_clicked, *q = pygame.mouse.get_pressed()

            if is_clicked:
                self.__move_dice(screen, board)

    def __move_dice(self, screen, board):
        """Перемещение фишки по полю"""
        x, y = pygame.mouse.get_pos()
        i = int(x / self.RECT_SIZE)
        j = int(y / self.RECT_SIZE)
        pos = j*self.DICE_ON_SIDE+i
        n = board[pos]

        if n != self.DICE_COUNT:
            empty_pos = board.index(self.DICE_COUNT)
            if empty_pos in [pos-1, pos+1, pos+self.DICE_ON_SIDE, pos-self.DICE_ON_SIDE]:
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
            if point == self.DICE_COUNT:
                total = total + int(pos / self.DICE_ON_SIDE) + 1
            else:
                last.append(point)
                for p in range(1, point):
                    if p not in last:
                        total = total + 1

        return total % 2 == 0

    def __generate_board(self):
        """Генерация фишек"""
        board = list(range(1, self.DICE_COUNT + 1))
        random.shuffle(board)
        return board if self.check_board(board) else self.__generate_board()

    def render(self, screen, board):
        screen.fill(self.BLACK)

        pos = -1
        for n in board:
            pos = pos + 1
            j = int(pos / self.DICE_ON_SIDE)
            i = pos % self.DICE_ON_SIDE

            if n == self.DICE_COUNT:
                continue

            x = self.RECT_SIZE * i + self.BORDER_WIDTH
            y = self.RECT_SIZE * j + self.BORDER_WIDTH
            width = self.RECT_SIZE - self.BORDER_WIDTH * (2 if i == 3 else 1)
            height = self.RECT_SIZE - self.BORDER_WIDTH * (2 if j == 3 else 1)

            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(screen, [136, 136, 136], rect)

            label = self.MY_FONT.render(str(n), 1, (220, 220, 220))
            screen.blit(label, (x + width/2 - label.get_width()/2, y + height/2 - label.get_height()/2))

        pygame.display.flip()

    def check_win(self, screen, board):
        for i in range(1, self.DICE_COUNT + 1):
            if i != board[i-1]:
                break
            if i == self.DICE_COUNT:
                label = pygame.font.SysFont('monospace', 82).render('WIN', 1, (220, 10, 10))
                screen.blit(label, (self.WIDTH/2 - label.get_width()/2, self.HEIGTH/2 - label.get_height()/2))
                pygame.display.flip()
