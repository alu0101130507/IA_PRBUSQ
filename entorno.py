import pygame
import random
from datetime import datetime

print(  "\nInstrucciones de uso:"
        "\nPara añadir obstáculos (sólo en modo manual) haga click derecho en la celda deseada."
        "\nPara marcar el inicio y final de la trayectoria haga click izquierdo."
        "\nPara empezar la búsqueda pulse espacio."
        "\nPara reiniciar el tablero pulse R."
        "\n¿De qué tamaño desea la tabla (M x N)?" 
        "Dependiendo del monitor que use habrá un máximo de celdas que se puedan visualizar\nM: ")
tablaM = int(input())
print("N: ")
tablaN = int(input())
print("¿Desea que la posición de los obstáculos sea manual (1) o aleatoria (2)?")
done = False
while done == False:
  obstMode = int(input())
  if obstMode == 1:
    manual = True
    done = True
  elif obstMode == 2:
    manual = False
    done = True
  else: 
    print("Valor introducido no válido. Introduzca 1 o 2.")

pygame.init()
random.seed(datetime.now())

screen_height = 1080
screen_width = 1920
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

icon = pygame.image.load("./hexagon.png")
pygame.display.set_caption("Búsqueda")
pygame.display.set_icon(icon)

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
    if self.state == 0:
      pygame.draw.rect(screen, (0, 0, 0), self.sprite)
    elif self.state == 1:
      pygame.draw.rect(screen, (255, 255, 255), self.sprite)
    elif self.state == 2:
      pygame.draw.rect(screen, (102, 178, 255), self.sprite)
    elif self.state == 3:
      pygame.draw.rect(screen, (255, 178, 102), self.sprite)

class Board:
  
  def __init__(self, rows_, cols_):
    self.rows = rows_ + 2
    self.cols = cols_ + 2
    self.turn = 0
    self.sprite = pygame.Rect(0.05 * screen_width, 0.05 * screen_height, self.cols*17, self.rows*17)
    self.mesh = []

    for i in range(self.rows):
      row = []
      for j in range(self.cols):
        rect = pygame.Rect(0.05 * screen_width + j*(15 + 2), 0.05 * screen_height + i*(15 + 2), 15, 15)
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

  def setCellState(self, state, posX, posY):
    givenCell = self.mesh[posX + 1][posY + 1]
    givenCell.state = state

  def killAll(self):
    for i in range(self.rows):
      for j in range(self.cols):
        self.mesh[i][j].state = 0
  
  def randomGen(self):
    for i in range(1, int((tablaM * tablaN)/10)):
      tabla.setCellState(1, random.randint(0, tablaM), random.randint(0, tablaN))

tabla = Board(tablaM, tablaN)
if manual == False:
  tabla.randomGen()

running = True
playing = False

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      posList = list(pos)
      posList[0] = pos[0] - 15
      posList[1] = pos[1] - 15
      if tabla.sprite.collidepoint(posList):
        for i in range(1, tabla.rows - 1):
          for j in range(1, tabla.cols - 1):
            temp_sprite = tabla.mesh[i][j].sprite
            if temp_sprite.collidepoint(posList):
              if event.button == 3:
                if manual == True:
                  tabla.setCellState(1, i, j)
              elif event.button == 1:
                tabla.setCellState(2, i, j)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        if (playing == False):
          playing = True
        else:
          playing = False
      if event.key == pygame.K_r:
        if manual == False:
          tabla.killAll()
          tabla.randomGen()
        else:
          tabla.killAll()

  screen.fill((80, 80, 80))
  tabla.printBoard()
  if playing == True:
    tabla.updateBoard()
  pygame.display.update()
