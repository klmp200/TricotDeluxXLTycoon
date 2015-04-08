# -*- coding: utf8 -*-
import json
import Core
import pygame
import sys
from pygame.locals import *
from Core import *
from Core.vaisseau import *
from Core.interfaces import *
from Core.videos import *

TITRE = "Tricot Delux XL Tycoon"
ICONE = "pelote.jpg"
RESOLUTION = (1200, 800)


# Importation des paramètres
json_data=open(r'config.json', 'r', encoding="utf8")
#json_data=open(r'config.json', 'r')
SETTINGS = json.load(json_data)
json_data.close()

pygame.init()

intro = Video('intro.mpg', SETTINGS, TITRE, ICONE, "2001_Odysee_de_l_espace.wav")
intro.jouer()

menu = Menu(RESOLUTION, "main_menu_background.png", TITRE, ICONE, SETTINGS, "star_wars.wav")
sortie = menu.pause()


fenetre = Jeu(RESOLUTION, "saucisses.jpg", TITRE, ICONE, SETTINGS, 'retour_futur.wav')

#Chargement de la banane
banane = Joueur((200,100), "banane.png", (0,int(fenetre.taille[1]/2-100)), SETTINGS, vitesse=20, pv = 10)

if sortie == "Facile":
	fenetre.limite = 3
elif sortie == "Normal":
	fenetre.limite = 10
elif sortie == "Hard":
	fenetre.limite = 40
elif sortie == "Dubstep":
	fenetre = Jeu(RESOLUTION, "espace.jpg", TITRE, ICONE, SETTINGS, 'hight_quality_dubstep.wav')
	fenetre.limite = 666

	fenetre.ennemiImage = "illuminati.png"
	fenetre.ennemiMissileImage = "confirmed.png"

	banane = Joueur((200,100), "doritos.png", (0,int(fenetre.taille[1]/2-100)), SETTINGS, vitesse=20, pv = 10)
	banane.imageMissile = "doritos_chips.png"

elif sortie == "Banana":
	fenetre = Jeu(RESOLUTION, "banana_back.jpg", TITRE, ICONE, SETTINGS, 'banana.wav')
	fenetre.limite = 10

	fenetre.ennemiImage = "banane.png"
	fenetre.ennemiMissileImage = "banane.png"

	banane.imageMissile = "banane.png"
elif sortie == "Poulet":
	fenetre = Jeu(RESOLUTION, "rainbow.jpg", TITRE, ICONE, SETTINGS, 'my_little_chicken.wav')
	fenetre.limite = 10

	fenetre.ennemiImage = "colonel.png"
	fenetre.ennemiMissileImage = "police.png"

	banane = Joueur((200,100), "charles.png", (0,int(fenetre.taille[1]/2-100)), SETTINGS, vitesse=20, pv = 10)
	banane.imageMissile = "poulet.png"

banane.afficher(fenetre.fenetre)
fenetre.pause(banane)