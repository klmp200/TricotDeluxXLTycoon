# -*- coding: utf8 -*-
import pygame
import random
import time
import sys
from pygame.locals import *
from Core.vaisseau import Ennemi, Modificateur

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

		# Ajouter la boucle

class Menu(Interface):

	def __init__(self, taille=(640, 480), image="", titre="", icone="", SETTINGS={}, musique=""):
		Interface.__init__(self, taille, image, titre, icone, SETTINGS, musique)
		self.menu_base = [
			(True, "Jouer", (True, "modes_jeu")),
			(False, "Extra", (True, "extra")),
			(False, "Crédits", (True, "credits")),
		]
		self.modes_jeu = [
			(True, "Facile", (False, "end")),
			(False, "Normal", (False, "end")),
			(False, "Hard", (False, "end")),
			(False, "Dubstep", (False, "end")),
			(False, "Banana", (False, "end")),
			(False, "Poulet", (False, "end")),
		]
		self.credits = [
			(False, "Réalisé et produit par :", (False, "non")),
			(False, "Antoine Bartuccio", (False, "non")),
			(False, "(KLMP200)", (False, "non")),
			(False, "klmp200.net", (False, "non")),
		]
		self.extra = [
			(True, "Flappy Banana", (False, "end")),
			(False, "Entrainement", (False, "end")),
		]

	def textMenu(self, liste):
		title_color = (22, 150, 22)
		main_color = (239, 119, 6)
		selected_color = (255, 255, 255)

		y = 0

		text = self.font.render("Menu", True, title_color)
		x = int(self.taille[0]/2) - int(text.get_width()/2)
		self.fenetre.blit(text, (x,y))

		y += text.get_height()*2
		
		for phrase in liste:
			color = main_color
			if phrase[0]:
				color = selected_color

			text = self.font.render(phrase[1], True, color)
			x = int(self.taille[0]/2) - int(text.get_width()/2)
			self.fenetre.blit(text, (x,y))
			y += text.get_height()

	def selectionMenu(self, direction, liste):
		if direction != "":
			s = 1
			for phrase in liste:
				if phrase[0]:
					break
				s += 1

			if direction == "UP":
				s = s-1
			elif direction == "DOWN":
				s = s+1

			if s > len(liste):
				s = len(liste)
			elif s < 1:
				s = 1

			new_liste = []
			p = 1
			for phrase in liste:
				if phrase[0]:
					phrase = (False, phrase[1], phrase[2])
				if p == s:
					phrase = (True, phrase[1], phrase[2])
				
				new_liste.append(phrase)
				p += 1
			liste = new_liste

		return liste

	def validerMenu(self, validation, menu):
		sortie = ""
		continuer = True
		if validation:
			for phrase in menu:
				if phrase[0] and phrase[2][0]:
					if phrase[2][1] == "modes_jeu":
						menu = self.modes_jeu
					elif phrase[2][1] == "credits":
						menu = self.credits
					elif phrase[2][1] == "extra":
						menu = self.extra
				if phrase[0] and not phrase[2][0]:
					if phrase[2][1] == "end":
						sortie = phrase[1]
						continuer = False

		return (menu, continuer, sortie)

	def retourMenu(self, retour, menu):
		if retour:
			menu = self.menu_base
		return menu


	def pause(self):
		Interface.pause(self)
		pygame.key.set_repeat()

		# Initialisation menu
		menu = self.menu_base
		sortie = ""

		continuer = True
		clock = pygame.time.Clock()
		while continuer:
			clock.tick(10)
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = False     #On arrête la boucle
					sys.exit()

				direction = ""
				validation = False
				retour = False
				if event.type == KEYDOWN:
					if event.key == K_DOWN:
						direction = "DOWN"

					if event.key == K_UP:
						direction = "UP"

					if event.key == K_BACKSPACE:
						retour = True

					if event.key == K_RETURN or event.key == K_SPACE:
						validation = True

			self.afficherBack()

			menu = self.selectionMenu(direction, menu)
			self.textMenu(menu)

			(menu, continuer, sortie) = self.validerMenu(validation, menu)
			menu = self.retourMenu(retour, menu)

			pygame.display.flip()

		self.musique.stop()
		return sortie	

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
		self.limite = 3

		self.liste_modificateurs = []
		self.limite_modificateurs = 2
		self.bonus_image = "bonus.png"
		self.malus_image = "malus.png"

		self.ennemiImage = "mouton.png"
		self.ennemiMissileImage = "chat.png"

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
		limite = self.limite
		aleatoire1 = random.randint(1,60)
		aleatoire2 = random.randint(1,100)
		if aleatoire2 < aleatoire1 and len(self.liste_ennemies) < limite:
			ennemi = Ennemi((200,100), self.ennemiImage, (random.randint(int(self.taille[1]/2),self.taille[1]+200),random.randint(0,self.taille[0]-100)), self.SETTINGS)
			ennemi.imageMissile = self.ennemiMissileImage
			self.liste_ennemies.append(ennemi)

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

	def generateModificateur(self):
		limite = self.limite_modificateurs
		pv = 0
		vitesse = 0
		vitesseMissile = 0

		chance = random.randint(0, 10)
		if chance < 4:
			# Bonus
			image = self.SETTINGS['IMAGES_DIR'] + self.bonus_image
			pv = random.randint(0, 3)
			vitesse = random.randint(0, 10)
			vitesseMissile = random.randint(0, 10)
		else:
			# Malus
			image = self.SETTINGS['IMAGES_DIR'] + self.malus_image
			pv = random.randint(0, 3)*(-1)
			vitesse = random.randint(0, 10)*(-1)
			vitesseMissile = random.randint(0, 10)*(-1)

		if len(self.liste_modificateurs) < limite:
			position = (random.randint(0,int(self.taille[1]/2)),random.randint(0,self.taille[0]-100))
			modificateur = Modificateur(position=position, image=image, pv=pv, vitesse=vitesse, vitesseMissile=vitesseMissile)
			self.liste_modificateurs.append(modificateur)

	def afficherModificateur(self, vaisseau):
		for modificateur in self.liste_modificateurs:
			modificateur.afficher(self.fenetre, vaisseau)

	def supprimerModificateur(self):
		i = 0
		to_pop = []
		for modificateur in self.liste_modificateurs:
				if modificateur.vie == False:
					to_pop.append(i)
				i += 1
		for crap in to_pop:
			self.liste_modificateurs.pop(crap)

	def pause(self, vaisseau):
		Interface.pause(self)
		pygame.key.set_repeat(30, 30)

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
			self.generateModificateur()

			vaisseau.afficher(self.fenetre)
			self.bougerBords()
			self.afficherVie(vaisseau)
			self.afficherScore()

			self.afficherEnnemi()
			self.afficherModificateur(vaisseau)
			self.actionEnnemi()
			self.tirerEnnemi(vaisseau)

			vaisseau.checkMissiles(self.fenetre, self.taille, victimes = self.liste_ennemies)
			self.supprimerEnnemi()
			self.supprimerModificateur()

			pygame.display.flip()

			if vaisseau.vie == False:
				continuer = False

		continuer = True
		explosion = pygame.image.load(self.SETTINGS['IMAGES_DIR'] + "boom.png").convert_alpha()
		explosion = pygame.transform.scale(explosion, self.taille)
		phraseMort = self.font.render(random.choice(self.deadPunchline ), True, (255,255,255))
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

class Message(Interface):
	def pause():
		pass