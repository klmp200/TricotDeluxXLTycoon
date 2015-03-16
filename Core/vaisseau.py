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

		self.repliques = [
			"Voilà qui tranche la question",
			"T'avais faim hein ?",
			"BANANA !!!!",
			"Bêêêê t'es mort !!!!",
			"get reckt LMAO EZ SCRUB !",
			"Miaou ? Ta geule miaou !",
			"Sponsorisé par Dominos Pizza",
			"Sponsorisé pas Pizza Hut",
			"Tu ne passera pas !",
			"J'espère que tu avais faim",
			"Même ma grand mère se serait mieux débrouillé !",
			"Tien, attrape !",
			"Trouve toi une autre prairie",
			"On se retrouvera en enfer !",
			"C'est pas ma guerre !!!!",
			"Ceci est une punchline",
			"Ca rentre comme papa dans maman",
			"KAMEHAMEPIZAAAAAAAAAA !!!!!!!",
			"Tu la voulait supplément fromage ?",
			"Plus rapide qu'un livreur de pizza traditionnel",
			"Toc Toc, c'est le livreur de pizza",
			"Qui a demandé une livreur de pizza ?",
			"C'est pour qui la quatre fromages ?",
			"C'est bien ici la livraison ?",
		]

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
		self.afficher(interface.fenetre, self.position)

class Joueur(Vaisseau):

	"""
		Pour fabriquer un joueur, hérite de la classe vaisseaux
	"""

	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}):
		Vaisseau.__init__(self, taille, image, position, SETTINGS)
		self.sonDeplacement = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + 'wut.ogg')

	def afficher(self, fenetre, position=""):
		self.sonDeplacement.play()
		Vaisseau.afficher(self, fenetre, position)

	def tirer(self, fenetre, tailleInterface):
		missile = Missile("pizza.png", (self.position[0]+self.taille[0], self.position[1]), (100,100), "piou.ogg", self.SETTINGS)
		missile.avancer(fenetre, 'left', tailleInterface)

class Ennemi(Vaisseau):
	"""
		Pour fabriquer des ennemies
	"""
	def __init__(self, taille=(0,0), image="", position=(0,0), SETTINGS={}):
		Vaisseau.__init__(self, taille, image, position, SETTINGS)
		self.sonDeplacement = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + 'la.ogg')

	def afficher(self, fenetre, position=""):
		self.sonDeplacement.play()
		Vaisseau.afficher(self, fenetre, position)

	def tirer(self, fenetre, tailleInterface):
		missile = Missile("chat.png", (self.position[0]+self.taille[0], self.position[1]), (100,100), "beeh.ogg", self.SETTINGS)
		missile.avancer(fenetre, 'right', tailleInterface)

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

		self.missile = pygame.image.load(self.sprite).convert_alpha()
		self.missile = pygame.transform.scale(self.missile, self.taille)

	def afficher(self, fenetre, position=""):
		if position != "":
			self.position = position

		fenetre.blit(self.missile, self.position)
		pygame.display.flip()
		self.son.play()

	def avancer(self, fenetre, origin, tailleInterface):
		x = self.position[0]
		y = self.position[1]

		continuer = True
		while continuer:
			if origin == "left":
				x += 10

			elif origin == "right":
				x += -10

			self.afficher(fenetre, (x,y))

			if x <= 0 or x >= tailleInterface[0]:
				continuer = False


