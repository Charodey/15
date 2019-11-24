import sys
import random

import pygame

class Game15:
    SIZE = WIDTH, HEIGTH = 400, 400
    BLACK = 0, 0, 0
    BORDER_WIDTH = 5
    RECT_SIZE = WIDTH * .25

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Пятнашки")
        self.MY_FONT = pygame.font.SysFont("monospace", 48)

    def start(self):
        screen = pygame.display.set_mode(self.SIZE)
        board = Game15.__generate_board()
        self.render(screen, board)
        self.__process(screen, board)

    def __process(self, screen, board):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            is_clicked, *q = pygame.mouse.get_pressed()

            if is_clicked:
                x, y = pygame.mouse.get_pos()
                i = int(x / self.RECT_SIZE)
                j = int(y / self.RECT_SIZE)
                pos = j*4+i
                n = board[pos]

                if n != 16:
                    empty_pos = board.index(16)
                    if empty_pos in [pos-1, pos+1, pos+4, pos-4]:
                        board[empty_pos], board[pos] = board[pos], board[empty_pos]
                        self.render(screen, board)
                        self.check_win(screen,board)

    @staticmethod
    def __check_board(board):
        '''Проверяем, что сгенерированный набор фишек - решаем'''
        last = []
        total = 0
        pos = -1
        for point in board:
            pos = pos + 1
            if point == 16:
                total = total + int(pos / 4) + 1
            else:
                last.append(point)
                for p in range(1, point):
                    if p not in last:
                        total = total + 1

        return total % 2 == 0

    @staticmethod
    def __generate_board():
        '''Генерация фишек'''
        board = list(range(1, 17))
        random.shuffle(board)
        return board if Game15.__check_board(board) else Game15.__generate_board()

    def render(self, screen, board):
        screen.fill(self.BLACK)

        pos = -1
        for n in board:
            pos = pos + 1
            j = int(pos / 4)
            i = pos % 4

            if n == 16:
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
        for i in range(1, 17):
            if i != board[i-1]:
                break
            if i == 16:
                label = pygame.font.SysFont('monospace', 82).render('WIN', 1, (220, 10, 10))
                screen.blit(label, (self.WIDTH/2 - label.get_width()/2, self.HEIGTH/2 - label.get_height()/2))
                pygame.display.flip()
