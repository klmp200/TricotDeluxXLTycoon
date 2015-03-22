# -*- coding: utf8 -*-
import pygame
import random
import time
import sys
from pygame.locals import *
from Core.vaisseau import Ennemi

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
		self.font = pygame.font.SysFont("comicsansms", 70)
		if icone != "":
			icone = pygame.image.load(self.SETTINGS['IMAGES_DIR'] + icone)
			pygame.display.set_icon(icone)

	def changerBackground(self, taille="", image=""):
		if taille != "" and image != "":
			self.taille = taille
			self.image = SETTINGS['IMAGES_DIR'] + image

		self.background = pygame.image.load(self.image).convert()
		self.background = pygame.transform.scale(self.background, self.taille)

	def afficherBack(self):
		self.fenetre.blit(self.background, (0,0))


	def pause(self):

		self.musique.play(loops=-1, maxtime=0, fade_ms=0)
		pygame.key.set_repeat(30, 30)

		# Ajouter la boucle

class menu(Interface):

	def __init__(self, taille=(640, 480), image="", titre="", icone="", SETTINGS={}, musique=""):
		Interface.__init__(self, taille, image, titre, icone, SETTINGS, musique)
		self.choix = [
			(True, "Jouer", ["Facile", "Normal", "Hard", "Dubstep"]),
			(True, "Crédits", ["Réalisé et produit par :", "Antoine Bartuccio", "(KLMP200)", "klmp200.net"]),
			(False, "Extra", ["Flappy Banana"]),
		]

class Jeu(Interface):

	def __init__(self, taille=(640, 480), image="", titre="", icone="", SETTINGS={}, musique=""):
		Interface.__init__(self, taille, image, titre, icone, SETTINGS, musique)
		self.bordure_taille = (1200, 50)
		self.bordure_image = pygame.image.load(self.SETTINGS['IMAGES_DIR'] + 'bordure.png').convert_alpha()
		self.bordure_haut_pos = (0, 0)
		self.bordure_bas_pos = (0, self.taille[1])

		self.fenetre.blit(self.bordure_image, (0,0))
		self.fenetre.blit(self.bordure_image, (0,self.taille[1]-50))

		self.score = 0

		self.liste_ennemies = []

		self.punchline = SETTINGS['PUNCHLINES']
		for punchline in self.punchline:
			punchline = punchline.encode('utf-8')

		self.deadPunchline = SETTINGS['MORT']
		for deadPunchline in self.deadPunchline:
			deadPunchline = deadPunchline.encode('utf-8')

	def bougerBords(self):
		vitesse = 15
		if self.bordure_haut_pos[0] < -self.bordure_taille[0]:
			# Réinitialise la position de la bordure mouvante
			self.bordure_haut_pos = (0, self.bordure_haut_pos[1])
			self.bordure_bas_pos = (0, self.bordure_bas_pos[1])
		else:
			# Donne une nouvelle position à la bordure
			self.bordure_haut_pos = (self.bordure_haut_pos[0]-vitesse, self.bordure_haut_pos[1])
			self.bordure_bas_pos = (self.bordure_bas_pos[0]-vitesse, self.bordure_bas_pos[1])

		# Bordure qui se colle à la fin de la bordure mouvante
		self.fenetre.blit(self.bordure_image, (self.bordure_taille[0]+self.bordure_bas_pos[0],0))
		self.fenetre.blit(self.bordure_image, (self.bordure_taille[0]+self.bordure_bas_pos[0],self.taille[1]-50))
		# Bordure mouvante
		self.fenetre.blit(self.bordure_image, (self.bordure_bas_pos[0],0))
		self.fenetre.blit(self.bordure_image, (self.bordure_bas_pos[0],self.taille[1]-50))

	def afficherVie(self, vaisseau):
		text = self.font.render("Vies : "+ str(vaisseau.pv), True, (229, 0, 0))
		self.fenetre.blit(text, (0,0))

	def afficherScore(self):
		text = self.font.render("Score : "+ str(self.score), True, (104, 0, 255))
		self.fenetre.blit(text, (int(self.taille[0]/2),0))

	def generateEnnemi(self):
		limite = 3
		aleatoire1 = random.randint(1,60)
		aleatoire2 = random.randint(1,100)
		if aleatoire2 < aleatoire1 and len(self.liste_ennemies) < limite:
			self.liste_ennemies.append(Ennemi((200,100), "mouton.png", (random.randint(int(self.taille[1]/2),self.taille[1]+200),random.randint(0,self.taille[0]-100)), self.SETTINGS))

	def afficherEnnemi(self):
		for ennemi in self.liste_ennemies:
			ennemi.afficher(self.fenetre)

	def actionEnnemi(self):
		for ennemi in self.liste_ennemies:
			ennemi.action(self)

	def tirerEnnemi(self, vaisseau):
		for ennemi in self.liste_ennemies:
			ennemi.checkMissiles(self.fenetre, self.taille, victimes = [vaisseau])

	def supprimerEnnemi(self):
		i = 0
		to_pop = []
		for ennemi in self.liste_ennemies:
			if ennemi.vie == False:
				to_pop.append(i)
			i += 1
		for crap in to_pop:
			self.liste_ennemies.pop(crap)
			self.score += 50
			
			text = self.font.render(random.choice(self.punchline), True, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
			self.fenetre.blit(text, (0,random.randint(0,self.taille[1]-70)))
			pygame.display.flip()
			time.sleep(1)


	def pause(self, vaisseau):
		Interface.pause(self)

		continuer = True
		clock = pygame.time.Clock()
		while continuer:
			clock.tick(60)
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = False     #On arrête la boucle
					sys.exit()

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


			self.afficherBack()
			self.generateEnnemi()

			vaisseau.afficher(self.fenetre)
			self.bougerBords()
			self.afficherVie(vaisseau)
			self.afficherScore()

			self.afficherEnnemi()
			self.actionEnnemi()
			self.tirerEnnemi(vaisseau)

			vaisseau.checkMissiles(self.fenetre, self.taille, victimes = self.liste_ennemies)
			self.supprimerEnnemi()

			pygame.display.flip()

			if vaisseau.vie == False:
				continuer = False

		continuer = True
		explosion = pygame.image.load(self.SETTINGS['IMAGES_DIR'] + "boom.png").convert_alpha()
		explosion = pygame.transform.scale(explosion, self.taille)
		phraseMort = self.font.render(random.choice(self.deadPunchline ), True, (0,0,0))
		while continuer:

			for event in pygame.event.get():
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = False     #On arrête la boucle
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_RETURN:
						continuer = False

			self.afficherBack()
			self.fenetre.blit(explosion, (0,0))

			self.afficherVie(vaisseau)
			self.afficherScore()

			self.fenetre.blit(phraseMort, (int(self.taille[0]/2) - int(phraseMort.get_width()/2), int(self.taille[1]/2)))

			pygame.display.flip()