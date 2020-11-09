import pygame
import random
import math
import time
from datetime import datetime

# Inicio del programa que muestra las instrucciones y deja al usuario personalizar la búsqueda

print(  "\nInstrucciones de uso:"
        "\nPara añadir obstáculos (sólo en modo manual) haga click derecho en la celda deseada."
        "\nPara marcar el inicio y final de la trayectoria haga click izquierdo."
        "\nPara empezar la búsqueda o pausarla pulse espacio."
        "\nPara reiniciar el tablero pulse R."
        "\n¿De qué tamaño desea la tabla (M x N)? " 
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
print("¿Desea utilizar la función heurística con la distancia Manhattan (1) o con la distancia Euclídea (2)?")
done = False
while done == False:
  hMode = int(input())
  if hMode == 1:
    done = True
  elif hMode == 2:
    done = True
  else: 
    print("Valor introducido no válido. Introduzca 1 o 2.")

# Inicialización de las variables necesarias para pygame.

pygame.init()
random.seed(datetime.now())

screen_height = 1080
screen_width = 1920
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

icon = pygame.image.load("./hexagon.png")
pygame.display.set_caption("Búsqueda")
pygame.display.set_icon(icon)

# Declaración de las clases que usaremos: Celda y Tabla.

class Cell:
    
  def __init__(self, position, state, sprite):
    self.position = position
    self.state = state
    self.sprite = sprite
    self.g = 0
    self.h = 0
    self.f = 0
    self.parent = None
    self.successors = []

  def draw(self):
    if self.state == 0:
      pygame.draw.rect(screen, (0, 0, 0), self.sprite)
    elif self.state == 1:
      pygame.draw.rect(screen, (255, 255, 255), self.sprite)
    elif self.state == 2:
      pygame.draw.rect(screen, (102, 178, 255), self.sprite)
    elif self.state == 3:
      pygame.draw.rect(screen, (255, 178, 102), self.sprite)
    elif self.state == 4:
      pygame.draw.rect(screen, (255, 255, 102), self.sprite)
    elif self.state == 5:
      pygame.draw.rect(screen, (255, 102, 102), self.sprite)

  def kill(self):
    self.state = 0
    self.g = 0
    self.h = 0
    self.f = 0
    self.parent = None
    self.successors.clear()

class Board:
  
  def __init__(self, rows_, cols_):
    self.rows = rows_ + 2                                                                                 # Número de filas de la tabla M
    self.cols = cols_ + 2                                                                                 # Número de columnas de la tabla N
    self.sprite = pygame.Rect(0.05 * screen_width, 0.05 * screen_height, self.cols*12, self.rows*12)      # Sprite del fondo de la tabla
    self.mesh = []                                                                                        # Cuadrícula donde irán las filas de celdas
    self.ends = []                                                                                        # Lista con el inicio (ends[0]) y el final (ends[1]) del recorrido

    for i in range(self.rows):
      row = []
      for j in range(self.cols):
        rect = pygame.Rect(0.05 * screen_width + j*(10 + 2), 0.05 * screen_height + i*(10 + 2), 10, 10)
        row.append(Cell([i, j], 0, rect))
      self.mesh.append(row)
    
  def printBoard(self):
    pygame.draw.rect(screen, (55, 55, 55), self.sprite)
    for i in range(1, self.rows - 1):
      for j in range(1, self.cols - 1):
        if self.mesh[i][j] in self.ends:
          self.mesh[i][j].state = 2
        elif self.mesh[i][j] in path:
          self.mesh[i][j].state = 5
        elif self.mesh[i][j] in openList:
          self.mesh[i][j].state = 4
        elif self.mesh[i][j] in closedList:
          self.mesh[i][j].state = 3
        self.mesh[i][j].draw()

  def toggleCellState(self, posX, posY):
    givenCell = self.mesh[posX + 1][posY + 1]

    if givenCell.state == 1:
      givenCell.state = 0
    else:
      givenCell.state = 1

  def setEnds(self, posX, posY):
    givenCell = self.mesh[posX + 1][posY + 1]
    givenCell.state = 2
    self.ends.append(givenCell)

  def killAll(self):
    for i in range(self.rows):
      for j in range(self.cols):
        self.mesh[i][j].kill()
    self.ends.clear()
    openList.clear()
    closedList.clear()
    path.clear()
  
  def randomGen(self):
    for _ in range(1, int((tablaM * tablaN)/5)):
      tabla.mesh[random.randint(0,tablaM)][random.randint(0,tablaN)].state = 1
  
  def calculateHeuristics(self, source):
    if hMode == 1:
      h = abs(source.position[0] - self.ends[1].position[0]) + abs(source.position[1] - self.ends[1].position[1]) 
    elif hMode == 2:
      h = math.sqrt((source.position[0] - self.ends[1].position[0])** 2 + (source.position[1] - self.ends[1].position[1])** 2)
    return h

  def returnPath(self, lastNode):
    path.clear()
    tempNode = lastNode
    path.append(tempNode)
    while tempNode.parent != None:
      path.append(tempNode.parent)
      tempNode = tempNode.parent

  def aStarSearch(self):
    minimum = 0
    for i in range(len(openList)):
      if openList[i].f < openList[minimum].f:
        minimum = i

    currentNode = openList.pop(minimum)
    closedList.append(currentNode)

    if currentNode == self.ends[1]:
      self.returnPath(currentNode)
      self.printBoard()
      print("Encontrado")
      return True

    for i in range(-1, 2):
      for j in range(-1, 2):
        currentNeighbor = self.mesh[currentNode.position[0] + i][currentNode.position[1] + j]
        if (i + j == 1 or i + j == -1) and currentNeighbor.state != 1 and not (currentNeighbor in 
        closedList) and not (currentNeighbor.position[0] > self.rows - 2 or currentNeighbor.position[1] > self.cols - 2):
          currentNode.successors.append(currentNeighbor)
          currentNeighbor.parent = currentNode

    for successor in currentNode.successors:
      tempG = currentNode.g + 1
      newPath = False
      if successor in openList:
        if tempG < successor.g:
          successor.g = tempG
          newPath = True
      else:
        successor.g = tempG
        newPath = True
        openList.append(successor)
      
      if newPath:
        
        successor.h = tabla.calculateHeuristics(successor)
        successor.f = successor.g + successor.h
        successor.parent = currentNode

    self.returnPath(currentNode)

    return False

# Variables a inicializar antes de realizar la búsqueda.

tabla = Board(tablaM, tablaN)
if manual == False:
  tabla.randomGen()

running = True
playing = False
found = False
currentNode = None
openList = []
closedList = []
path = []

# Bucle en el que se irá actualizando la tabla mediante el input que reciba del usuario.

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN and playing == False:
      pos = pygame.mouse.get_pos()
      posList = list(pos)
      posList[0] = pos[0] - 15
      posList[1] = pos[1] - 15
      if tabla.sprite.collidepoint(posList):
        for i in range(0, tabla.rows - 2):
          for j in range(0, tabla.cols - 2):
            temp_sprite = tabla.mesh[i][j].sprite
            if temp_sprite.collidepoint(posList):
              if event.button == 3 and manual == True:
                tabla.toggleCellState(i,j)
              elif event.button == 1 and len(tabla.ends) < 2:
                tabla.setEnds(i, j)
                if len(tabla.ends) == 2:
                  currentNode = tabla.ends[0]
                  openList.append(currentNode)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE and len(tabla.ends) == 2:
        start = time.time()
        if (playing == False):
          playing = True
        else:
          playing = False
      if event.key == pygame.K_r and playing == False:
        found = False
        if manual == False:
          tabla.killAll()
          tabla.randomGen()
        else:
          tabla.killAll()

  screen.fill((80, 80, 80))
  tabla.printBoard()

  if playing and len(tabla.ends) == 2 and found == False:
    if openList:
      found = tabla.aStarSearch()
      if found == True:
        end = time.time()
        playing = False

        print("Número de nodos recorridos:\t", len(closedList))
        print("Longitud del camino mínimo:\t", len(path))
        print("Tiempo empleado (s):\t\t", end-start)
    else:
      print("No se ha encontrado solución.")
      playing = False
  pygame.display.update()
