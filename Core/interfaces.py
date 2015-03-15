# -*- coding: utf8 -*-
import json
import pygame
from pygame.locals import *

class Interface():

	"""
		Une classe pour fabriquer des fenêtres
	"""

	def __init__(self, taille=(640, 480), image="", titre="", icone=""):
		self. taille = taille
		self.image = image
		self.fenetre = pygame.display.set_mode(taille, RESIZABLE)
		self.titre = titre
		self.background = ""
		self.changerBackground()
		pygame.display.set_caption(self.titre)
		if icone != "":
			icone = pygame.image.load(icone)
			pygame.display.set_icon(icone)

	def changerBackground(self, taille="", image=""):
		if taille != "" and image != "":
			self.taille = taille
			self.image = image

		self.background = pygame.image.load(self.image).convert()
		self.background = pygame.transform.scale(self.background, self.taille)

	def afficher(self):
		self.fenetre.blit(self.background, (0,0))
		pygame.display.flip()

	def pause(self, vaisseau):
		continuer = 1
		pygame.key.set_repeat(30, 30)
		while continuer:
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = 0      #On arrête la boucle

				mouvement = ""

				if event.type == KEYDOWN:
					if event.key == K_DOWN:	#Si "flèche bas"
						mouvement = "DOWN"

					if event.key == K_UP:
						mouvement = "UP"

					if event.key == K_RIGHT:
						mouvement = "RIGHT"

					if event.key == K_LEFT:
						mouvement = "LEFT"

					self.fenetre.blit(self.background, (0,0))
					vaisseau.deplacer(self, mouvement)