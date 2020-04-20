import pygame, sys
import numpy as np
import time

pygame.init()

width, height = 901, 901
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25

nxC, nyC = 90, 90

dimCW = (width) / nxC
dimCH = (height) / nyC

# Estados de las celdas. Vivas = 1; muertas = 0
gameState = np.zeros((nxC, nyC))


# Automata movil
gameState[10,10] = 1
gameState[11,11] = 1
gameState[12,11] = 1
gameState[12,10] = 1
gameState[12,9] = 1

pauseExect = False
grid = True


newGameState = np.copy(gameState)

while True:

	#newGameState = np.copy(gameState)
	time.sleep(0.01)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		# Para pausar el juego
		if event.type == pygame.KEYDOWN:
			pauseExect = not pauseExect

	# Para activar/desactivar celdas con el raton
	mouseClick = pygame.mouse.get_pressed()
	if sum(mouseClick) > 0:
		posX, posY = pygame.mouse.get_pos()
		celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH)) 
		newGameState[celX, celY] = not mouseClick[2]


	screen.fill(bg)

	for y in range(0, nxC):
		for x in range(0, nyC):

			#Calculamos el numero de vecinas vivas
			n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
					  gameState[(x)     % nxC, (y - 1) % nyC] + \
					  gameState[(x + 1) % nxC, (y - 1) % nyC] + \
					  gameState[(x - 1) % nxC, (y)     % nyC] + \
					  gameState[(x + 1) % nxC, (y)     % nyC] + \
					  gameState[(x - 1) % nxC, (y + 1) % nyC] + \
					  gameState[(x)     % nxC, (y + 1) % nyC] + \
					  gameState[(x + 1) % nxC, (y + 1) % nyC]

			# Pausa el juego (Solo evito que evolucione segun las reglas, el resto de las instrucciones si se ejecutan)
			if not pauseExect:

				# Regla 1: Una celda muerta con exactamente 3 vecinas vivas, "revive"
				if gameState[x, y] == 0 and n_neigh == 3:
					newGameState[x, y] = 1

				# Regla 2: Una celda viva con menos de 2 o mas de 3 vecinas vivas, "muere"
				elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
					newGameState[x, y] = 0


			# dibujamos la celda para cada par x, y
			poly = [((x)     * dimCW, y * dimCH),
					((x + 1) * dimCW, y * dimCH),
					((x + 1) * dimCW, (y + 1) * dimCH),
					((x)     * dimCW, (y + 1) * dimCH)]

			if newGameState[x, y] == 0:
				if grid:
					pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
			else:
				pygame.draw.polygon(screen, (128, 128, 128), poly, 0)


	# Actualizamos el estado del juego
	gameState = np.copy(newGameState)

	# Actualizamos la pantalla
	pygame.display.flip()