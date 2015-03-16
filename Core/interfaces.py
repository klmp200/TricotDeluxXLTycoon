# -*- coding: utf8 -*-
import pygame
from pygame.locals import *

class Interface():

	"""
		Une classe pour fabriquer des fenêtres
	"""

	def __init__(self, taille=(640, 480), image="", titre="", icone="", SETTINGS={}, musique=""):
		self.SETTINGS = SETTINGS
		self. taille = taille
		self.image = SETTINGS['IMAGES_DIR'] + image
		self.fenetre = pygame.display.set_mode(taille)
		self.titre = titre
		self.background = ""
		self.musique = pygame.mixer.Sound(self.SETTINGS['SONS_DIR'] + musique)
		self.changerBackground()
		pygame.display.set_caption(self.titre)
		if icone != "":
			icone = pygame.image.load(self.SETTINGS['IMAGES_DIR'] + icone)
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

	def pause(self):

		pygame.time.Clock().tick(60)

		self.musique.play(loops=-1, maxtime=0, fade_ms=0)
		pygame.key.set_repeat(30, 30)

		# Ajouter la boucle

class Jeu(Interface):

	def __init__(self, taille=(640, 480), image="", titre="", icone="", SETTINGS={}, musique=""):
		Interface.__init__(self, taille, image, titre, icone, SETTINGS, musique)
		self.bordure_taille = (1200, 50)
		self.bordure_image = pygame.image.load(self.SETTINGS['IMAGES_DIR'] + 'bordure.png').convert_alpha()
		self.bordure_haut_pos = (0, 0)
		self.bordure_bas_pos = (0, self.taille[1])

		self.fenetre.blit(self.bordure_image, (0,0))
		self.fenetre.blit(self.bordure_image, (0,self.taille[1]-50))

	def bougerBords(self):
		if self.bordure_haut_pos[0] < -self.bordure_taille[0]:
			self.bordure_haut_pos = (0, self.bordure_haut_pos[1])
			self.bordure_bas_pos = (0, self.bordure_bas_pos[1])
		else:
			self.bordure_haut_pos = (self.bordure_haut_pos[0]-10, self.bordure_haut_pos[1])
			self.bordure_bas_pos = (self.bordure_bas_pos[0]-10, self.bordure_bas_pos[1])


		self.fenetre.blit(self.bordure_image, (self.bordure_bas_pos[0],0))
		self.fenetre.blit(self.bordure_image, (self.bordure_bas_pos[0],self.taille[1]-50))

	def generateEnnemi(self):
		pass

	def pause(self, vaisseau):
		Interface.pause(self)

		continuer = 1
		while continuer:
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = 0      #On arrête la boucle

				mouvement = ""
				tirer = False

				if event.type == KEYDOWN:
					if event.key == K_DOWN:
						mouvement = "DOWN"

					if event.key == K_UP:
						mouvement = "UP"

					if event.key == K_RIGHT:
						mouvement = "RIGHT"

					if event.key == K_LEFT:
						mouvement = "LEFT"

					if event.key == K_SPACE:
						tirer = True

					vaisseau.deplacer(self, mouvement)
					if tirer:
						vaisseau.tirer()

			self.fenetre.blit(self.background, (0,0))

			self.bougerBords()

			vaisseau.afficher(self.fenetre)
			vaisseau.checkMissiles(self.fenetre, self.taille)