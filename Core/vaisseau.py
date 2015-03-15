# -*- coding: utf8 -*-
import json
import pygame
from pygame.locals import *

class Vaisseau():

	"""
		Classe pour fabriquer des vaisseaux
	"""

	def __init__(self, taille=(0,0), image="", position=(0,0)):
		self.taille = taille
		self.image = image
		self.position = position
		self.changerImage()

	def changerImage(self, taille="", image=""):
		if taille != "" and image != "":
			self.taille = taille
			self.image = image

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

