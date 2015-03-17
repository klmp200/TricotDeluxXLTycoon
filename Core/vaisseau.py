# -*- coding: utf8 -*-
import pygame
import random
import time
from pygame.locals import *

class Vaisseau():

	"""
		Classe pour fabriquer des vaisseaux
	"""

	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}, vitesse=10, pv = 1):
		self.SETTINGS = SETTINGS
		self.taille = taille
		self.image = self.SETTINGS['IMAGES_DIR'] + image
		self.position = position
		self.changerImage()
		self.vitesse = vitesse
		self.vie = True
		self.pv = pv
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

	def deplacer(self, interface, direction="", origin="LEFT"):
		x = self.position[0]
		y = self.position[1]

		maxRight = 0
		maxLeft = 0
		if origin == "LEFT":
			maxRight = int(interface.taille[0]/2)-self.taille[0]
			maxLeft = 0

		elif origin == "RIGHT":
			maxRight = interface.taille[0]-self.taille[0]
			maxLeft = int(interface.taille[0]/2)

		if direction == "DOWN":
			if y+10 < interface.taille[1]-self.taille[1]:
				y = y+self.vitesse
		elif direction == "UP":
			if y+10 > 0:
				y = y-self.vitesse
		elif direction == "RIGHT":
			if x+10 < maxRight:
				x = x+self.vitesse
		elif direction == "LEFT":
			if x+10 > maxLeft:
				x = x-self.vitesse


		self.position = (x, y)

	def tirer(self, son="", image=""):
		self.missiles.append(Missile(image, (self.position[0]+self.taille[0], self.position[1]), (100,100), son, self.SETTINGS))

	def checkMissiles(self, fenetre, tailleInterface, direction, victimes = []):
		i = 0
		to_pop = []
		for missile in self.missiles:
			missile.avancer(fenetre, direction, tailleInterface, victimes)
			if missile.vie == False:
				to_pop.append(i)

		for crap in to_pop:
			self.missiles.pop(crap)

	def mort(self, fenetre, degats=1):
		self.pv -= degats
		if self.pv <= 0:
			self.vie = False
			explosion = pygame.image.load(self.SETTINGS['IMAGES_DIR'] + "boom.png").convert_alpha()
			explosion = pygame.transform.scale(explosion, self.taille)
			fenetre.blit(explosion, self.position)
			pygame.display.flip()
			time.sleep(.1)




class Joueur(Vaisseau):

	"""
		Pour fabriquer un joueur, hérite de la classe vaisseaux
	"""

	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}, vitesse=10, pv=1):
		Vaisseau.__init__(self, taille, image, position, SETTINGS, vitesse, pv)
		self.sonDeplacement = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + 'wut.ogg')

		self.punchline = SETTINGS['PUNCHLINES']
		for punchline in self.punchline:
			punchline = punchline.encode('utf-8')

	def checkMissiles(self, fenetre, tailleInterface, direction="left", victimes = []):
		Vaisseau.checkMissiles(self, fenetre, tailleInterface, direction, victimes)

	def deplacer(self, interface, direction=""):
		self.sonDeplacement.play()
		Vaisseau.deplacer(self, interface, direction)

	def tirer(self, son="piou.ogg", image="pizza.png"):
		Vaisseau.tirer(self, son, image)


class Ennemi(Vaisseau):
	"""
		Pour fabriquer des ennemies
	"""
	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}, vitesse=10, pv = 1):
		Vaisseau.__init__(self, taille, image, position, SETTINGS, vitesse, pv)
		self.sonDeplacement = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + 'la.ogg')


	def checkMissiles(self, fenetre, tailleInterface, direction="right", victimes = []):
		Vaisseau.checkMissiles(self, fenetre, tailleInterface, direction, victimes)

	def deplacer(self, interface, direction="", origin="RIGHT"):
		self.sonDeplacement.play()
		Vaisseau.deplacer(self, interface, direction, origin)

	def tirer(self, son="beeh.ogg", image="chat.png"):
		Vaisseau.tirer(self, son, image)

	def action(self, interface):
		choix = random.randint(1,50)
		if choix == 1:
			self.tirer()
		else:
			mouvement = ""
			direction = random.randint(1,4)

			if direction == 1:
				mouvement = "DOWN"

			if direction == 2:
				mouvement = "UP"

			if direction == 3:
				mouvement = "RIGHT"

			if direction == 4:
				mouvement = "LEFT"

			self.deplacer(interface, mouvement)
				

class Missile():
	"""
		Pour fabriquer des missiles
	"""

	def __init__(self, sprite, position, taille, son, SETTINGS, vitesse=5):
		self.SETTINGS = SETTINGS
		self.sprite = self.SETTINGS['IMAGES_DIR'] + sprite
		self.position = position
		self.taille = taille
		self.son = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + son)
		self.vie = True
		self.vitesse = vitesse

		self.missile = pygame.image.load(self.sprite).convert_alpha()
		self.missile = pygame.transform.scale(self.missile, self.taille)
		self.son.play()

	def afficher(self, fenetre, position=""):
		if position != "":
			self.position = position

		fenetre.blit(self.missile, self.position)

	def avancer(self, fenetre, origin, tailleInterface, victimes = []):
		x = self.position[0]
		y = self.position[1]

		if origin == "left":
			x += self.vitesse

		elif origin == "right":
			x += -self.vitesse

		self.afficher(fenetre, (x,y))

		if x <= 0 or x >= tailleInterface[0]:
			self.vie = False

		rect_missile = pygame.Rect(x, y, self.taille[0], self.taille[1])
		for victime in victimes:
			rect_victime = pygame.Rect(victime.position[0], victime.position[1], victime.taille[0], victime.taille[1])

			if rect_missile.colliderect(rect_victime):
				victime.mort(fenetre)
				self.vie = False
				break