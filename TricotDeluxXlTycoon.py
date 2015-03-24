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
SETTINGS = json.load(json_data)
json_data.close()

pygame.init()


intro = Video('intro.mpg', SETTINGS, TITRE, ICONE, "2001_Odysee_de_l_espace.wav")
intro.jouer()

fenetre = Jeu(RESOLUTION, "saucisses.jpg", TITRE, ICONE, SETTINGS, 'retour_futur.wav')

#Chargement de la banane
banane = Joueur((200,100), "banane.png", (0,int(fenetre.taille[1]/2-100)), SETTINGS, vitesse=20, pv = 10)
banane.afficher(fenetre.fenetre)


fenetre.pause(banane)