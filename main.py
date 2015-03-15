# -*- coding: utf8 -*-
import json
import Core
import pygame
from pygame.locals import *
from Core import *
from Core.vaisseau import *
from Core.interfaces import *

# Importation des paramètres
json_data=open(r'config.json', 'r')
SETTINGS = json.load(json_data)
json_data.close()

pygame.init()

fenetre = Interface((1200, 800), SETTINGS['IMAGES_DIR'] + "saucisses.jpg", "Tricot Delux XL Tycoon", SETTINGS['IMAGES_DIR'] + "pelote.jpg")
fenetre.afficher()

#Chargement de la banane
banane = Vaisseau((200,100), SETTINGS['IMAGES_DIR'] + "banane.png", (0,int(fenetre.taille[1]/2-100)))
banane.afficher(fenetre.fenetre)

fenetre.pause(banane)