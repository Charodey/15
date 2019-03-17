import sys, pygame, random

def check_board(board):
  last = []
  sum = 0
  pos = -1
  for point in board:
    pos = pos + 1
    if point == 16:
      sum = sum + int(pos / 4) + 1
    else:
      last.append(point)
      for p in range(1, point):
        if p not in last:
          sum = sum + 1

  return sum % 2 == 0

def generate():
  board = list(range(1, 17))
  random.shuffle(board)
  return board if check_board(board) else generate()

def render():
  screen.fill(black)

  pos = -1
  for n in board:
    pos = pos + 1
    j = int(pos / 4)
    i = pos % 4

    if n == 16:
      continue

    x = rectSize * i + borderWidth
    y = rectSize * j + borderWidth
    width = rectSize - borderWidth * (2 if i == 3 else 1)
    height = rectSize - borderWidth * (2 if j == 3 else 1)
    
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, [136,136,136], rect)

    label = myfont.render(str(n), 1, (220, 220, 220))
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

  myfont = pygame.font.SysFont("monospace", 48)

  size = width, height = 400, 400
  speed = [-1, 1]
  black = 0, 0, 0
  borderWidth = 5
  rectSize = width * .25

  screen = pygame.display.set_mode(size)
  
  board = generate()
  render()

  while 1:
      
      for event in pygame.event.get():
          if event.type == pygame.QUIT: sys.exit()
      
      isCLicked, *q = pygame.mouse.get_pressed()

      if isCLicked:
        x, y = pygame.mouse.get_pos()
        i = int(x / rectSize)
        j = int(y / rectSize)
        pos = j*4+i
        n = board[pos]

        if n != 16:
          emptyPos = board.index(16)
          if emptyPos in [pos-1, pos+1, pos+4, pos-4]:
            board[emptyPos], board[pos] = board[pos], board[emptyPos]
            render()
            check_win()