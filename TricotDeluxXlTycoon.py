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
json_data=open(r'config.json', 'r')
SETTINGS = json.load(json_data)
json_data.close()

pygame.init()


intro = Video('intro.mpg', SETTINGS, TITRE, ICONE, "2001_Odysee_de_l_espace.ogg")
intro.jouer()

fenetre = Jeu(RESOLUTION, "saucisses.jpg", TITRE, ICONE, SETTINGS, 'retour_futur.ogg')
fenetre.afficher()

#Chargement de la banane
banane = Joueur((200,100), "banane.png", (0,int(fenetre.taille[1]/2-100)), SETTINGS)
banane.afficher(fenetre.fenetre)

"""
#Test mouton
mouton = Ennemi((200,100), "mouton.png", (fenetre.taille[0]-200,int(fenetre.taille[1]/2-100)), SETTINGS)
mouton.afficher(fenetre.fenetre)
"""

fenetre.pause(banane)