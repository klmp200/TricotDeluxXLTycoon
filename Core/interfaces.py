# -*- coding: utf8 -*-
import pygame
from pygame.locals import *

class Interface():

	"""
		Une classe pour fabriquer des fenêtres
	"""

	def __init__(self, taille=(640, 480), image="", titre="", icone="", SETTINGS={}):
		self.SETTINGS = SETTINGS
		self. taille = taille
		self.image = SETTINGS['IMAGES_DIR'] + image
		self.fenetre = pygame.display.set_mode(taille)
		self.titre = titre
		self.background = ""
		self.musique = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + 'retour_futur.ogg')
		self.changerBackground()
		pygame.display.set_caption(self.titre)
		if icone != "":
			icone = pygame.image.load(SETTINGS['IMAGES_DIR'] + icone)
			pygame.display.set_icon(icone)

	def changerBackground(self, taille="", image=""):
		if taille != "" and image != "":
			self.taille = taille
			self.image = SETTINGS['IMAGES_DIR'] + image

		self.background = pygame.image.load(self.image).convert()
		self.background = pygame.transform.scale(self.background, self.taille)

	def afficher(self):
		self.fenetre.blit(self.background, (0,0))
		pygame.display.flip()

	def pause(self, vaisseau):
		self.musique.play(loops=-1, maxtime=0, fade_ms=0)
		continuer = 1
		pygame.key.set_repeat(30, 30)
		while continuer:
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = 0      #On arrête la boucle

				mouvement = ""
				tirer = False

				if event.type == KEYDOWN:
					if event.key == K_DOWN:	#Si "flèche bas"
						mouvement = "DOWN"

					if event.key == K_UP:
						mouvement = "UP"

					if event.key == K_RIGHT:
						mouvement = "RIGHT"

					if event.key == K_LEFT:
						mouvement = "LEFT"

					if event.key == K_SPACE:
						tirer = True

					self.fenetre.blit(self.background, (0,0))
					vaisseau.deplacer(self, mouvement)
					if tirer:
						vaisseau.tirer(self.fenetre, self.taille)