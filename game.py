import sys
import random

import pygame


def check_board(board):
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

def generate():
    '''Генерация фишек'''
    board = list(range(1, 17))
    random.shuffle(board)
    return board if check_board(board) else generate()

def render():
    screen.fill(BLACK)

    pos = -1
    for n in board:
        pos = pos + 1
        j = int(pos / 4)
        i = pos % 4

        if n == 16:
            continue

        x = RECT_SIZE * i + BORDER_WIDTH
        y = RECT_SIZE * j + BORDER_WIDTH
        width = RECT_SIZE - BORDER_WIDTH * (2 if i == 3 else 1)
        height = RECT_SIZE - BORDER_WIDTH * (2 if j == 3 else 1)

        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, [136, 136, 136], rect)

        label = MY_FONT.render(str(n), 1, (220, 220, 220))
        screen.blit(label, (x + width/2 - label.get_width()/2, y + height/2 - label.get_height()/2))

    pygame.display.flip()

def check_win():
    for i in range(1, 17):
        if i != board[i-1]:
            break
        if i == 16:
            label = pygame.font.SysFont('monospace', 82).render('WIN', 1, (220, 10, 10))
            screen.blit(label, (width/2 - label.get_width()/2, height/2 - label.get_height()/2))
            pygame.display.flip()


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption("Пятнашки")

    MY_FONT = pygame.font.SysFont("monospace", 48)

    SIZE = width, height = 400, 400
    BLACK = 0, 0, 0
    BORDER_WIDTH = 5
    RECT_SIZE = width * .25

    screen = pygame.display.set_mode(SIZE)

    board = generate()
    render()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        is_clicked, *q = pygame.mouse.get_pressed()

        if is_clicked:
            x, y = pygame.mouse.get_pos()
            i = int(x / RECT_SIZE)
            j = int(y / RECT_SIZE)
            pos = j*4+i
            n = board[pos]

            if n != 16:
                empty_pos = board.index(16)
                if empty_pos in [pos-1, pos+1, pos+4, pos-4]:
                    board[empty_pos], board[pos] = board[pos], board[empty_pos]
                    render()
                    check_win()
