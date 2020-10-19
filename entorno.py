import pygame

pygame.init()

screen_height = 1080
screen_width = 1920
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
icon = pygame.image.load("./hexagon.png")

pygame.display.set_caption("Life")
pygame.display.set_icon(icon)

play = pygame.image.load("./play.png")
playX = 0.03 * screen_width
playY = 0.2 * screen_height
font = pygame.font.Font(pygame.font.get_default_font(), 16)
textEsp = font.render("\"Espacio\"", True, (0, 0, 0))
textEspRect = textEsp.get_rect()
textEspRect.center = (0.045 * screen_width, 0.28 * screen_height)

refresh = pygame.image.load("./refresh.png")
refreshX = 0.03 * screen_width
refreshY = 0.4 * screen_height
textR = font.render("\"R\"", True, (0, 0, 0))
textRRect = textR.get_rect()
textRRect.center = (0.045 * screen_width, 0.48 * screen_height)

class Cell:
    
  def __init__(self, position, state, sprite):
    self.position = position
    self.state = state
    self.neighbors = 0
    self.sprite = sprite

  def count(self, Board):
    counted = 0
    for i in range(-1, 2):
      for j in range(-1, 2):
        if not(i == 0 and j == 0):
          if Board.mesh[self.position[0] + i][self.position[1] + j].state == 1:
            counted += 1
    self.neighbors = counted

  def update(self):
    if self.state == 1:
      if self.neighbors == 2 or self.neighbors == 3:
        self.state = 1
      else:
        self.state = 0
    elif self.state == 0 and self.neighbors == 3:
      self.state = 1

  def draw(self):
    if self.state == 1:
      pygame.draw.rect(screen, (255, 255, 255), self.sprite)
    else:
      pygame.draw.rect(screen, (0, 0, 0), self.sprite)

class Board:
  
  def __init__(self, rows_, cols_):
    self.rows = rows_ + 2
    self.cols = cols_ + 2
    self.turn = 0
    self.sprite = pygame.Rect(0.1 * screen_width, 0.1 * screen_height, 0.9 * screen_width - (0.1 * screen_width), 0.9 * screen_height - (0.1 * screen_height))

    self.mesh = []
    for i in range(self.rows):
      row = []
      for j in range(self.cols):
        rect = pygame.Rect(0.1 * screen_width + j*(10 + 2), 0.1 * screen_height + i*(10 + 2), 10, 10)
        row.append(Cell([i, j], 0, rect))
      self.mesh.append(row)
    
  def printBoard(self):
    pygame.draw.rect(screen, (55, 55, 55), self.sprite)
    for i in range(1, self.rows - 1):
      for j in range(1, self.cols - 1):
        self.mesh[i][j].draw()

  def updateBoard(self):
    for i in range(1, self.rows - 1):
      for j in range(1, self.cols - 1):
        self.mesh[i][j].count(self)
    for i in range(1, self.rows - 1):
      for j in range(1, self.cols - 1):
        self.mesh[i][j].update()
    self.turn += 1

  def toggleCellState(self, posX, posY):
    givenCell = self.mesh[posX + 1][posY + 1]

    if givenCell.state == 1:
      givenCell.state = 0
    else:
      givenCell.state = 1

  def killAll(self):
    for i in range(self.rows):
      for j in range(self.cols):
        self.mesh[i][j].state = 0

running = True
playing = False
tabla = Board(70,126)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      posList = list(pos)
      posList[0] = pos[0] - 10
      posList[1] = pos[1] - 10
      if tabla.sprite.collidepoint(posList):
        for i in range(1, tabla.rows - 1):
          for j in range(1, tabla.cols - 1):
            temp_sprite = tabla.mesh[i][j].sprite
            if temp_sprite.collidepoint(posList):
              tabla.toggleCellState(i, j)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        if (playing == False):
          play = pygame.image.load("./pause.png")
          playing = True
        else:
          play = pygame.image.load("./play.png")
          playing = False
      if event.key == pygame.K_r:
        tabla.killAll()


  screen.fill((80, 80, 80))
  screen.blit(play, (playX, playY))
  screen.blit(textEsp, textEspRect)
  screen.blit(textR, textRRect)
  screen.blit(refresh, (refreshX, refreshY))
  tabla.printBoard()
  if playing == True:
    tabla.updateBoard()
  pygame.display.update()