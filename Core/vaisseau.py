# -*- coding: utf8 -*-
import pygame
from pygame.locals import *

class Vaisseau():

	"""
		Classe pour fabriquer des vaisseaux
	"""

	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}):
		self.SETTINGS = SETTINGS
		self.taille = taille
		self.image = self.SETTINGS['IMAGES_DIR'] + image
		self.position = position
		self.changerImage()

		self.missiles = []

	def changerImage(self, taille="", image=""):
		if taille != "" and image != "":
			self.taille = taille
			self.image = SETTINGS['IMAGES_DIR'] + image

		self.vaisseau = pygame.image.load(self.image).convert_alpha()
		self.vaisseau = pygame.transform.scale(self.vaisseau, self.taille)

	def afficher(self, fenetre, position=""):
		if position != "":
			self.position = position

		fenetre.blit(self.vaisseau, self.position)
		pygame.display.flip()

	def deplacer(self, interface, direction=""):
		x = self.position[0]
		y = self.position[1]

		if direction == "DOWN":
			if y+10 < interface.taille[1]-self.taille[1]:
				y = y+10
		elif direction == "UP":
			if y+10 > 0:
				y = y-10
		elif direction == "RIGHT":
			if x+10 < int(interface.taille[0]/2)-self.taille[0]:
				x = x+10
		elif direction == "LEFT":
			if x+10 > 0:
				x = x-10
		else:
			pass

		self.position = (x, y)

	def tirer(self, son="", image=""):
		self.missiles.append(Missile(image, (self.position[0]+self.taille[0], self.position[1]), (100,100), son, self.SETTINGS))

	def checkMissiles(self, fenetre, tailleInterface, direction):
		i = 0
		to_pop = []
		for missile in self.missiles:
			missile.avancer(fenetre, direction, tailleInterface)
			if missile.vie == False:
				to_pop.append(i)

		for crap in to_pop:
			self.missiles.pop(crap)


class Joueur(Vaisseau):

	"""
		Pour fabriquer un joueur, hérite de la classe vaisseaux
	"""

	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}):
		Vaisseau.__init__(self, taille, image, position, SETTINGS)
		self.sonDeplacement = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + 'wut.ogg')

		self.punchline = SETTINGS['PUNCHLINES']
		for punchline in self.punchline:
			punchline = punchline.encode('utf-8')

	def checkMissiles(self, fenetre, tailleInterface, direction="left"):
		Vaisseau.checkMissiles(self, fenetre, tailleInterface, direction)

	def deplacer(self, interface, direction=""):
		self.sonDeplacement.play()
		Vaisseau.deplacer(self, interface, direction)

	def tirer(self, son="piou.ogg", image="pizza.png"):
		Vaisseau.tirer(self, son, image)


class Ennemi(Vaisseau):
	"""
		Pour fabriquer des ennemies
	"""
	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}):
		Vaisseau.__init__(self, taille, image, position, SETTINGS)
		self.sonDeplacement = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + 'la.ogg')


	def checkMissiles(self, fenetre, tailleInterface, direction="right"):
		Vaisseau.checkMissiles(self, fenetre, tailleInterface, direction)

	def deplacer(self, interface, direction=""):
		self.sonDeplacement.play()
		Vaisseau.deplacer(self, interface, direction)

	def tirer(self, son="beeh.ogg", image="chat.png"):
		Vaisseau.tirer(self, son, image)


class Missile():
	"""
		Pour fabriquer des missiles
	"""

	def __init__(self, sprite, position, taille, son, SETTINGS):
		self.SETTINGS = SETTINGS
		self.sprite = self.SETTINGS['IMAGES_DIR'] + sprite
		self.position = position
		self.taille = taille
		self.son = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + son)
		self.vie = True

		self.missile = pygame.image.load(self.sprite).convert_alpha()
		self.missile = pygame.transform.scale(self.missile, self.taille)
		self.son.play()

	def afficher(self, fenetre, position=""):
		if position != "":
			self.position = position

		fenetre.blit(self.missile, self.position)
		pygame.display.flip()

	def avancer(self, fenetre, origin, tailleInterface):
		x = self.position[0]
		y = self.position[1]

		if origin == "left":
			x += 10

		elif origin == "right":
			x += -10

		self.afficher(fenetre, (x,y))

		if x <= 0 or x >= tailleInterface[0]:
			self.vie = False
